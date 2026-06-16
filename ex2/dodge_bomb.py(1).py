import os
import sys
import time
import math
import random
import pygame as pg

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し、真理値タプルを返す関数
    引数 obj_rct：こうかとんRect、または、爆弾Rect
    戻り値：横方向、縦方向のはみ出し判定結果（画面内：True ／ 画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:#ゲームオーバー画面
    """
    ゲームオーバー画面を表示する関数
    引数 screen：画面Surface
    """
    # 半透明の黒い画面を作成して上書き
    bg_black = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_black, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bg_black.set_alpha(128)
    
    # "Game Over" の文字列を作成
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    
    # 泣いているこうかとん（8.png）を左右に配置
    kk_img = pg.image.load("fig/8.png") 
    kk_rct1 = kk_img.get_rect()
    kk_rct1.center = WIDTH // 2 - 200, HEIGHT // 2
    kk_rct2 = kk_img.get_rect()
    kk_rct2.center = WIDTH // 2 + 200, HEIGHT // 2
    
    # 各要素を画面に描画
    screen.blit(bg_black, [0, 0])
    screen.blit(txt, txt_rct)
    screen.blit(kk_img, kk_rct1)
    screen.blit(kk_img, kk_rct2)
    
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceのリストと加速度リストを返す関数
    戻り値：爆弾Surfaceリスト、加速度リストのタプル
    """
    bb_imgs: list[pg.Surface] = []
    bb_accs: list[int] = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs
#def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
   # """
   # サイズの異なる爆弾Surfaceのリストと加速度リストを返す関数
    #戻り値：爆弾Surfaceリスト、加速度リストのタプル
   # """
   # bb_imgs = []
    #bb_accs = [a for a in range(1, 11)]
    #for r in range(1, 11):
        #bb_img = pg.Surface((20 * r, 20 * r))
        #bb_img.set_colorkey((0, 0, 0))
        #pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        #bb_imgs.append(bb_img)
    #return bb_imgs, bb_accs
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量に対応するこうかとん画像の辞書を返す関数
    戻り値：移動量タプルをキー、こうかとんSurfaceを値とする辞書
    """
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img1 = pg.transform.flip(img0, True, False)  # 右向きベース
    return {
        (0, 0): img0,    # 静止時は左向き（初期状態用）
        (-5, 0): img0,   # 左
        (-5, -5): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
        (0, -5): pg.transform.rotozoom(img1, 90, 1.0),    # 上
        (+5, -5): pg.transform.rotozoom(img1, 45, 1.0),   # 右上
        (+5, 0): img1,    # 右
        (+5, +5): pg.transform.rotozoom(img1, -45, 1.0),  # 右下
        (0, +5): pg.transform.rotozoom(img1, -90, 1.0),   # 下
        (-5, +5): pg.transform.rotozoom(img0, 45, 1.0)    # 左下
    }




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()