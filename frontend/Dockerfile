# 构建阶段
FROM node:20-alpine as build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 重新加载Nginx配置
RUN nginx -s reload || true

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
