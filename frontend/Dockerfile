FROM node:14.16.1-alpine3.13
COPY ./ /app
WORKDIR /app
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
# 安装依赖
RUN cnpm install

# 打包 - 目的：丢到nginx下跑
RUN cnpm run build:prod

FROM nginx:1.15.2-alpine
RUN mkdir /app
COPY --from=0 /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
