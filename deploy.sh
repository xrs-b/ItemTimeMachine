#!/bin/bash

# ItemTimeMachine 一键部署脚本

set -e

echo "=========================================="
echo "  ItemTimeMachine 一键部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
check_docker() {
    echo -n "检查 Docker... "
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓ 已安装${NC}"
        docker --version
    else
        echo -e "${RED}✗ 未安装${NC}"
        echo "请先安装 Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
}

# 检查Docker Compose是否安装
check_docker_compose() {
    echo -n "检查 Docker Compose... "
    if command -v docker compose &> /dev/null || command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✓ 已安装${NC}"
    else
        echo -e "${RED}✗ 未安装${NC}"
        echo "请先安装 Docker Compose"
        exit 1
    fi
}

# 检查git是否安装
check_git() {
    echo -n "检查 Git... "
    if command -v git &> /dev/null; then
        echo -e "${GREEN}✓ 已安装${NC}"
    else
        echo -e "${RED}✗ 未安装${NC}"
        echo "请先安装 Git"
        exit 1
    fi
}

# 检查端口是否被占用
check_port() {
    echo -n "检查端口 80 和 8888... "
    if lsof -i:80 &> /dev/null || lsof -i:8888 &> /dev/null; then
        echo -e "${YELLOW}⚠ 端口可能被占用${NC}"
    else
        echo -e "${GREEN}✓ 端口正常${NC}"
    fi
}

# 克隆或更新代码
update_code() {
    echo ""
    echo "=========================================="
    echo "  更新代码"
    echo "=========================================="
    
    # 判断当前目录是否有ItemTimeMachine
    if [ -d "/var/www/ItemTimeMachine" ]; then
        echo "更新现有代码..."
        cd /var/www/ItemTimeMachine
        git pull
    elif [ -d "$(dirname "$0")/.git" ]; then
        echo "当前目录已是项目目录"
    else
        echo "克隆项目代码..."
        mkdir -p /var/www
        cd /var/www
        git clone https://github.com/xrs-b/ItemTimeMachine.git
        cd ItemTimeMachine
    fi
}

# 构建和启动
deploy() {
    echo ""
    echo "=========================================="
    echo "  构建并启动服务"
    echo "=========================================="
    
    # 停止旧服务
    echo "停止旧服务..."
    docker compose down 2>/dev/null || true
    
    # 构建并启动
    echo "构建镜像..."
    docker compose build --no-cache
    
    echo "启动服务..."
    docker compose up -d
    
    # 等待服务启动
    echo "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    echo ""
    echo "=========================================="
    echo "  检查服务状态"
    echo "=========================================="
    docker compose ps
    
    # 测试API
    echo ""
    echo "测试后端API..."
    if curl -s http://localhost:8888/health | grep -q "ok"; then
        echo -e "${GREEN}✓ 后端服务正常${NC}"
    else
        echo -e "${YELLOW}⚠ 后端服务可能未就绪，请稍后检查${NC}"
    fi
    
    # 测试前端
    echo "测试前端..."
    if curl -s http://localhost | grep -q "html"; then
        echo -e "${GREEN}✓ 前端服务正常${NC}"
    else
        echo -e "${YELLOW}⚠ 前端服务可能未就绪，请稍后检查${NC}"
    fi
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  deploy     执行完整部署（默认）"
    echo "  update     仅更新代码"
    echo "  restart    重启服务"
    echo "  logs       查看日志"
    echo "  status     查看服务状态"
    echo "  help       显示帮助信息"
    echo ""
}

# 主菜单
main() {
    # 环境检查
    echo ""
    echo "=========================================="
    echo "  环境检查"
    echo "=========================================="
    check_docker
    check_docker_compose
    check_git
    check_port
    
    case "${1:-deploy}" in
        deploy)
            update_code
            deploy
            ;;
        update)
            update_code
            ;;
        restart)
            cd /var/www/ItemTimeMachine
            docker compose restart
            ;;
        logs)
            cd /var/www/ItemTimeMachine
            docker compose logs -f
            ;;
        status)
            cd /var/www/ItemTimeMachine
            docker compose ps
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
    
    echo ""
    echo "=========================================="
    echo -e "  ${GREEN}部署完成！${NC}"
    echo "=========================================="
    echo ""
    echo "访问地址:"
    echo "  前端: http://你的服务器IP"
    echo "  后端: http://你的服务器IP:8888"
    echo ""
    echo "常用命令:"
    echo "  查看日志: $0 logs"
    echo "  查看状态: $0 status"
    echo "  重启服务: $0 restart"
    echo ""
}

# 运行
main "$@"
