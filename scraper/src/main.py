import contextlib
import os
import pymysql
import playwright
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page, expect
import json
from concurrent.futures import ThreadPoolExecutor
import requests
import io
from PIL import Image

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USERNAME = os.environ.get("DB_USERNAME")

URL = "https://www.simplyfitness.com"
GUIDES_URL = f"{URL}/pages/workout-exercise-guides"


@contextlib.contextmanager
def connect_sql():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        db=DB_NAME,
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        yield cursor
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.commit()
        connection.close()


def custom_strip(text):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    t = text.translate(translator)
    return t.strip()


def get_categories(page: Page):
    main = page.locator(".content-main").first
    container = main.locator("div").first
    categories = container.locator(".grid-item").all()

    d = {}
    for category in categories:
        category_anchor = category.locator("a").first
        name = category_anchor.text_content().strip()
        links = []

        exercises = category.locator("ul").locator("li").all()

        for exercise in exercises:
            anchor = exercise.locator("a").first
            link = anchor.get_attribute("href")
            links.append(link)

        d[name] = links

    return d


def get_next_text(page, text, element=None, timeout=1500):
    try:
        if element:
            header = page.locator(f"{element}:has-text('{text}')").first
        else:
            header = page.locator(f"text={text}").first
        header.wait_for(timeout=timeout)

        # Locate the first following sibling
        element = header.locator("xpath=following-sibling::*[1]").first
        element.wait_for(timeout=timeout)

        return custom_strip(element.text_content())
    except:
        return None


def get_next_element(page, text, element=None, timeout=500):
    try:
        if element:
            header = page.locator(f"{element}:has-text('{text}')").first
        else:
            header = page.locator(f"text={text}").first
        header.wait_for(timeout=timeout)

        # Locate the first following sibling
        element = header.locator("xpath=following-sibling::*[1]").first
        element.wait_for(timeout=timeout)

        return element
    except:
        return None


def scrape_exercise(page, exercises, link):
    page.goto(f"{URL}{link}")

    exercise = {}

    # get exercise name
    name = custom_strip(page.locator("h1").text_content())
    exercise["name"] = name

    # get exercise starting position
    start_position = get_next_text(page, "Starting position", "h3")
    exercise["start_position"] = start_position

    # get equipment required
    equipment_required = get_next_text(page, "Equipment required")
    if equipment_required:
        equipment_required = equipment_required.split(",")
        equipment_required = [custom_strip(i) for i in equipment_required]
        exercise["equipment_required"] = equipment_required

    # get execution
    execution = get_next_text(page, "Execution", "h3")
    steps_element = get_next_element(page, "During the whole movement:")

    # get execution steps
    steps = []
    if steps_element:
        lis = steps_element.locator("li").all()
        for li in lis:
            steps.append(custom_strip(li.text_content()))

    exercise["execution"] = {"main": execution, "steps": steps}
    return exercise



def scrape_category(page, name, links):
    exercises = {
    }
    for link in links:
        exercise = scrape_exercise(page, exercises, link)
        exercises[exercise["name"]] = exercise

    return exercises



def db_commit():
    filenames = [
        "Abdominals.json",
        "Back.json",
        "Biceps.json",
        "Chest.json",
        "Legs.json",
        "Calves.json"
    ]

    for file_name in filenames:
        with open(file_name, "r") as file:
            exercises = json.load(file)

        with connect_sql() as cursor:
            for name, exercise in exercises.items():
                print(exercise)

                # Insert into exercise table
                qry = """
                    INSERT INTO exercise (name, start_position, main_muscle)
                    VALUES (%s, %s, %s)
                """
                values = (name, exercise["start_position"], file_name.split(".json")[0])
                cursor.execute(qry, values)
                exercise_id = cursor.lastrowid

                # Insert equipment if required
                if "equipment_required" in exercise:
                    for equipment in exercise["equipment_required"]:
                        # Corrected Tuple Issue
                        qry = "SELECT * FROM equipment WHERE name = %s"
                        values = (equipment,)  # Ensure tuple format
                        cursor.execute(qry, values)
                        exists = cursor.fetchone()

                        if not exists:
                            qry = """
                                INSERT INTO equipment (name)
                                VALUES (%s)
                            """
                            values = (equipment)
                            cursor.execute(qry, values)
                            equipment_id = cursor.lastrowid
                            qry = """
                                INSERT INTO exercise_equipment (exercise_id, equipment_id)
                                VALUES (%s, %s)
                            """
                            cursor.execute(qry, (exercise_id, equipment_id))
                        else:
                            qry = """
                                INSERT INTO exercise_equipment (exercise_id, equipment_id)
                                VALUES (%s, %s)
                            """
                            values = (exercise_id, exists["id"])

                # Insert execution description
                qry = """
                    INSERT INTO execution (description, exercise_id)
                    VALUES (%s, %s)
                """
                values = (exercise["execution"]["main"], exercise_id)
                cursor.execute(qry, values)
                execution_id = cursor.lastrowid

                # Insert step details
                qry = """
                    INSERT INTO step (description, number, execution_id)
                    VALUES (%s, %s, %s)
                """
                for count, step in enumerate(exercise["execution"]["steps"]):
                    values = (step, count, execution_id)
                    cursor.execute(qry, values)

def to_kebab(string):
    return "-".join(string.strip().lower().split())

def img_url():
    with connect_sql() as cursor:
        qry = """
            SELECT * FROM exercise
        """
        cursor.execute(qry)
        exercises = cursor.fetchall()

        qry = """
            UPDATE exercise
            SET img_url = %s
            WHERE id = %s
        """
        for exercise in exercises:
            values = (f"{exercise['main_muscle'].lower()}/{to_kebab(exercise['name'])}", exercise["id"])
            cursor.execute(qry, values)
def img_down(muscle, exercise, link):
    try:
        response = requests.get(link).content
        img_file = io.BytesIO(response)  # Convert response to a file-like object
        image = Image.open(img_file)  # Open the image correctly

        # Ensure the muscle directory exists
        muscle = muscle.lower()
        os.makedirs(muscle, exist_ok=True)

        # Save the image
        img_path = f"{muscle}/{to_kebab(exercise)}.png"
        with open(img_path, "wb") as f:
            image.save(f, "PNG")
            print(f"Saved: {img_path}")
    except Exception as e:
        print(f"Error downloading {exercise}: {e}")

def download():
    with open("links.json", "r") as file:
        links = json.load(file)

    # Prepare tasks for executor
    tasks = [
        (muscle, exercise, link)
        for muscle, exercises in links.items()
        for exercise, link in exercises.items()
    ]

    # Download images in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda args: img_down(*args), tasks)


def scrape_images(headless=True):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=headless)
        page = browser.new_page()
        page.goto(GUIDES_URL)

        categories = get_categories(page)
        imgs = {}
        for muscle, category in categories.items():
            for link in category:
                name = custom_strip(page.locator("h1").text_content())
                page.goto(f"{URL}{link}")
                all_imgs = page.locator("img").all()
                
                if not imgs.get(muscle):
                    imgs[muscle] = {}

                for img in all_imgs:
                    alt = img.get_attribute("alt")
                    if "illustration" in alt.lower():
                        src = img.get_attribute("src")
                        imgs[muscle][name] = src
                        print(src)

    with open("links.json", "w") as file:
        json.dump(imgs, file)


def main(headless=False, is_scraping=True):
    if is_scraping:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=headless)
            page = browser.new_page()
            page.goto(GUIDES_URL)

            categories = get_categories(page)
            all = {}
            for key, category in categories.items():
                exercises = scrape_category(page, key, category)
                all[key] = exercises
    else:
        db_commit()


if __name__ == "__main__":
    #scrape_images()
    #download()
    img_url()
    #main(is_scraping=False)
