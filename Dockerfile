# Use an appropriate base image for your application
FROM node:16  # Change as needed for your language/framework

WORKDIR /app

# Copy dependency files first for better caching
COPY package*.json ./  
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application if needed
# RUN npm run build

# Expose the port your app runs on
EXPOSE 8000

# Command to run your application
CMD ["npm", "start"] 