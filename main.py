import numpy as np
import cv2
import pandas as pd
import os
import argparse

def load_existing_records(f):
    seen = {}
    if os.path.exists(f):
        try:
            seen = pd.read_csv(f, header=None, index_col=0).T.to_dict('list')
        except:
            pass
        good_cases = len([v[1] for v in seen.values() if v[1] == 1])
        print(f'Found {good_cases}/{len(seen)} records')
    else:
        pd.DataFrame({}).to_csv(f, index=False)
        print('found 0 records')
    return seen


def gather_imgs(root_dir):
    for root, _, files in os.walk(root_dir):
        for f in files:
            yield os.path.join(root, f)


def alpha_blend(src, mask, mask_opacity):
    src = src.astype('float64')
    src *= (1.0 / src.max())
    mask = mask.astype('float64')
    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    mask *= (1.0 / mask.max())
    return src * (1.0 - mask_opacity) + mask * mask_opacity


def append_to_file(seen:dict, f):
    res = ''.join([','.join([k, v[0], str(v[1])])+'\n' for k, v in seen.items()])
    with open(f, 'a+') as file:
        file.write(res)


def tag_images(f, clip_root, matting_root):
    seen_from_file = load_existing_records(f)

    # clip_root = './data/clip_img'
    # matting_root = './data/matting'

    seen = {}
    seen_clips, seen_mattings = [], []

    look_at = 0

    clip_collection = gather_imgs(clip_root)
    matting_collection = gather_imgs(matting_root)

    while True:
        if look_at >= len(seen_clips):
            while True:
                clip_path = next(clip_collection, None)
                matting_path = next(matting_collection, None)
                if clip_path not in seen_from_file:
                    break
        else:
            clip_path = seen_clips[look_at]
            matting_path = seen_mattings[look_at]
        if clip_path is None:
            break

        clip_img = cv2.imread(clip_path)
        mask = cv2.imread(matting_path, cv2.IMREAD_UNCHANGED)[:, :, 3]
        overlay_img = alpha_blend(clip_img, mask, 0.55)

        if clip_path in seen:
            if seen[clip_path][1] == 0:
                cv2.line(overlay_img, (100, 0), (0, 100), (0, 0, 255), 5)
                cv2.line(overlay_img, (0, 0), (100, 100), (0, 0, 255), 5)
            else:
                cv2.circle(overlay_img, (50, 50), 50, (0, 255, 0), 5)
        cv2.namedWindow('overlay', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('overlay', (clip_img.shape[1]//1, clip_img.shape[0]//1))
        cv2.imshow('overlay', overlay_img)
        press = cv2.waitKeyEx(0)
        if press == 27:
            append_to_file(seen, f)
            break
        elif press == 2555904:   # right key
            if clip_path not in seen:
                seen[clip_path] = (matting_path, 0)
                seen_clips.append(clip_path)
                seen_mattings.append(matting_path)
            look_at += 1
        elif press == 2424832:   # left key
            if clip_path not in seen:
                seen[clip_path] = (matting_path, 0)
                seen_clips.append(clip_path)
                seen_mattings.append(matting_path)
            look_at -= 1
            look_at = max(look_at, 0)
        elif press == 2490368:  # up key
            if clip_path not in seen:
                seen_clips.append(clip_path)
                seen_mattings.append(matting_path)
            seen[clip_path] = (matting_path, 1)
        else:
            if clip_path not in seen:
                seen_clips.append(clip_path)
                seen_mattings.append(matting_path)
            seen[clip_path] = (matting_path, 0)
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='Image filtering')
    parser.add_argument('clip_root', help='root path of clip images')
    parser.add_argument('matting_root', help='root path of matting images')
    args = parser.parse_args()

    f = './good_data.csv'
    tag_images(f, args.clip_root, args.matting_root)


if __name__ == '__main__':
    main()
