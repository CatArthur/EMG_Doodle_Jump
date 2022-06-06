import math

def intersect_x(y,x1,y1,x2,y2):
    if(x1==x2):
        return x1
    if(y1==y2):
        return math.inf
    k = (y1 - y2) / (x1 - x2)
    b = y2 - k*x2
    return (y-b)/k


def check_collison_top(plr_rect, p_plr_rect, blk_rect):
    if (p_plr_rect.bottom<=blk_rect.top)&(plr_rect.bottom>=blk_rect.top):
        lx = intersect_x(blk_rect.top,p_plr_rect.left,p_plr_rect.bottom,plr_rect.left,plr_rect.bottom)
        rx = intersect_x(blk_rect.top,p_plr_rect.right,p_plr_rect.bottom,plr_rect.right,plr_rect.bottom)
        return ((rx>=blk_rect.left)&(rx<=blk_rect.right)) | ((lx>=blk_rect.left)&(lx<=blk_rect.right))
    return False