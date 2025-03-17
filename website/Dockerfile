# Use Node.js 20 as the base image
FROM node:20

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json first for efficient caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Build the Vite app (output goes to `dist/`)
RUN npm run build

# Install `serve` globally to serve the built app
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Start the app using `serve`
CMD ["serve", "-s", "dist"]

