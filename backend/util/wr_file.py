"""
project: apiAutoTestWeb
file: wr_file.py
author: zy7y
date: 2021/4/18
desc: 读/写文件方法
"""
import aiofiles


async def read_file(path: str) -> str:
    """
    读取文件
    Args:
        path: 文件路径，

    Returns:
        result: 文件数据
    """
    async with aiofiles.open(path, "r", encoding="utf-8") as fp:
        return await fp.read()


async def write_file(path: str, data: str):
    """
    写文件
    Args:
        path: 文件路径
        data: 写入字符串

    Returns:

    """
    async with aiofiles.open(path, "w", encoding="utf-8") as fp:
        await fp.write(data)
