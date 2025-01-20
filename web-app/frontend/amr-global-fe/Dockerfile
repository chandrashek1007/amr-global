# Frontend Dockerfile
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire application
COPY . .

# Expose the default React development server port
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
