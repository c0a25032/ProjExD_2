import os
import random
import sys
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
    if obj_rct.left < 0 or WIDTH < obj_rct.right:#横方向
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の初期化
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))  # 黒い部分を透過させる
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い爆弾を描画
    bd_rct = bd_img.get_rect()#爆弾Rect
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の移動速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        # 衝突判定
        if kk_rct.colliderect(bd_rct):#重なったら
            print("ゲームオーバー！")
            return

        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]: sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]: sum_mv[1] += 5
        if key_lst[pg.K_LEFT]: sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]: sum_mv[0] += 5
        
        kk_rct.move_ip(sum_mv)
        # 画面外に出てしまったら元の位置に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            
        screen.blit(kk_img, kk_rct)

        # 爆弾の移動処理と壁での反射
        bd_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
            
        screen.blit(bd_img, bd_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()