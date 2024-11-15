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

### 至于说抄袭的一部分

抄袭点一:使用python
<br>抄袭点二:使用了pip
<br>抄袭点三:使用了舞萌DX的资源
<br>抄袭点四:依赖名称使用了`requirements.txt`
<br>抄袭点五:都是用了Pillow库和内置lib
<br>抄袭点六:居然做出来效果都和舞萌副屏玩家卡片类似
# 其次就是指着项目说抄袭的,说话的人是不是连github项目都没打开看一眼就说抄袭了，自己clone看看效果下来看看code跑一下看看效果或者不信邪去代码查重，在这之后再说抄袭我现在就去玩原神🤣
