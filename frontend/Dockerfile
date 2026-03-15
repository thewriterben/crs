# Multi-stage build for Frontend
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy workspace package files (root lockfile ensures reproducible builds)
COPY package.json package-lock.json ./
COPY frontend/package.json ./frontend/

# Install all dependencies including devDependencies for the build
RUN npm ci --workspace=frontend

# Copy frontend source code
COPY frontend/ ./frontend/

# Build the application
WORKDIR /app/frontend
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy custom nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /usr/share/nginx/html && \
    chown -R appuser:appuser /var/cache/nginx && \
    chown -R appuser:appuser /var/log/nginx && \
    chown -R appuser:appuser /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appuser /var/run/nginx.pid

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
