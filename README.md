# mai_draw

`mai_draw` 是用于绘制与舞萌dx玩家卡片相似的卡片的python项目

1. [安装](#安装)
2. [资源准备](#资源准备)
3. [使用示例](#示例)
4. [资源来源](#资源来源)

## 安装

克隆项目到本地；

```git
git clone https://github.com/gllc/mai_draw.git
```

依赖安装：

```sh 
pip install -r requirements.txt
```

## 资源准备

##### 1.通过[链接](https://1drv.ms/u/s!AoBHZVMZvJZscrX2KkyrMZUVlbc?e=IpRf1V)下载项目的资源文件

##### 2.指定资源目录

- 方式1.将`out`目录复制到项目根目录中

- 方式2.手动指定资源目录

```python
# file: draw.py line: 67
Res_Manager = ResourceManager(Path("your_resource_path"))
```

## 示例

#### 代码示例

```python
from draw import CardDraw, UserChara

if __name__ == '__main__':
    cd = CardDraw(
        name="gllc",
        icon=405703,
        title=405799,
        plate=405701,
        frame=405102,
        chara=[
            UserChara(characterId=400405, level=9999),
            UserChara(characterId=200201, level=9999),
            UserChara(characterId=400301, level=721),
            UserChara(characterId=601, level=1145),
            UserChara(characterId=355809, level=9999),
        ]
    )
    cd.draw()
    cd.get_image().save("example.png")
```

#### 输出结果

![example.png](example.png)

##### CardDraw类其他可选方法

| 方法          | 参数      | 用途   |
|-------------|---------|------|
| draw_rating | rating值 | 绘制评级 |
| draw_class  | classId | 绘制阶级 |
| draw_dan    | danId   | 绘制段位 |

- 参数类型均为int类型

## 资源来源

字体来源:群U
<br>图片来源:舞萌DX
