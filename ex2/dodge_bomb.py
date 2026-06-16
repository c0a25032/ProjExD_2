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
    font_size = 80
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
def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    爆弾からこうかとんへの方向ベクトルを計算する関数
    引数 org：爆弾Rect、dst：こうかとんRect、current_xy：現在の速度ベクトル
    戻り値：新しい速度ベクトル（vx, vyのタプル）
    """
    diff_x = dst.centerx - org.centerx
    diff_y = dst.centery - org.centery
    dist = math.sqrt(diff_x**2 + diff_y**2)
    
    # 距離が300未満の場合は追従せず、現在の慣性（速度）を維持
    if dist < 300:
        return current_xy
    
    # 差ベクトルのノルムが√50になるように正規化
    norm = math.sqrt(50)
    if dist > 0:
        vx = (diff_x / dist) * norm
        vy = (diff_y / dist) * norm
    else:
        vx, vy = current_xy
        
    return vx, vy


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    # try:
    unko_img = pg.image.load("fig/unko.png")
    unko_img = pg.transform.scale(unko_img, (50, 50)) # 50x50サイズに調整
    # except Exception as e:
    #     print(f"画像読み込みエラー: {e}")
    #     unko_img = pg.Surface((40, 40))
    #     unko_img.fill((139, 69, 19)) # 画像がない時の身代わり(茶色の四角)

    unko_list = []
    clock = pg.time.Clock()
    tmr = 0
    sum_mv = [0, 0]  # ループ開始前に初期化

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動キー入力受付
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]: sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]: sum_mv[1] += 5
        if key_lst[pg.K_LEFT]: sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]: sum_mv[0] += 5
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        # 移動しているときだけ画像を変更（静止時は直前の向きを維持）
        #if sum_mv != [0, 0]:
            #kk_img = kk_imgs[tuple(sum_mv)]
        kk_img = kk_imgs[(sum_mv[0], sum_mv[1])]
        screen.blit(kk_img, kk_rct)

        # ▽▽▽ ここから追加 ▽▽▽
        # 10秒に1回（50fpsなので500フレームごと）落とす処理
        if tmr > 0 and tmr % 500 == 0:
            new_unko_rct = unko_img.get_rect()
            new_unko_rct.center = kk_rct.center  # こうかとんの現在地
            unko_list.append(new_unko_rct)

        # 画面内の物体を下に移動させて描画（画面外に出たら削除）
        for u_rct in unko_list[:]:
            u_rct.move_ip(0, 4)  # 下方向に毎フレーム4ピクセルずつ落下
            if u_rct.top > HEIGHT:
                unko_list.remove(u_rct)
            else:
                screen.blit(unko_img, u_rct)

        # 追従型爆弾のベクトル計算
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))

        # 爆弾の拡大と加速
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        
        # 【修正】新しいSurfaceから正しくRectを生成し、中心座標を引き継ぐ
        bb_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = bb_center
        
        bb_rct.move_ip(avx, avy)
        
        # 壁での反射処理（めり込み防止対策込み）
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
            bb_rct.move_ip(-avx, 0)  # 1フレーム分位置を戻す
        if not tate:
            vy *= -1
            bb_rct.move_ip(0, -avy)  # 1フレーム分位置を戻す
            
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()