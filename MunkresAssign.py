
import numpy as np
from itertools import permutations

#cost_mat = np.array([[82, 83, 69, 92],
#          [77, 37, 49, 92],
#          [11, 69, 5, 86],
#          [8, 9, 98, 23]])
#cost_mat = np.array([[82, 74, 69, 87],
#          [36, 37, 49, 92],
#          [8, 69, 5, 86],
#          [8, 9, 98, 23]])
#cost_mat = np.array([[82, 74, 69, 87, 100],
#          [36, 37, 49, 92, 56],
#          [36, 37, 49, 92, 56],
#          [8, 69, 5, 86, 45],
#          [8, 9, 98, 23, 20]])
#cost_mat = np.array([[82, 74, 69, 87, 100],
#          [36, 37, 49, 36, 56],
#          [8, 69, 5, 86, 45],
#          [8, 9, 98, 23, 20]])
#cost_mat = np.array([
#          [8, 74, 5, 87, 20, 30],
#          [86, 9, 40, 23, 20, 79],
#          [8, 37, 90, 63, 20, 30],
#          [63, 9, 5, 23, 56, 56],
#          [8, 9, 35, 86, 23, 30],
#          [8, 69, 98, 23, 20, 60]])
#cost_mat = np.array([
#           [60, 19, 40, 12, 57, 69],
#           [55, 40, 15, 81, 49, 43],
#           [16, 82, 23, 58, 16, 27],
#           [38,  1, 17,  5, 11, 85],
#           [93,  9, 63, 17, 80, 21],
#           [23, 78,  3, 79, 72, 84]])
cost_mat = np.random.randint(1, high=1000, size=(10,9))
# print("cost_mat:\r\n", cost_mat)

#[[1, 0, 1, 0, 1, 1],
# [0, 1, 0, 1, 1, 0],
# [1, 0, 0, 0, 1, 1],
# [0, 1, 1, 1, 0, 0],
# [1, 1, 0, 0, 0, 1],
# [1, 0, 0, 1, 1, 0]]

def find_first_non_zero_item_idx(vector):
    idx_rs = None
    for idx, val in enumerate(vector):
        if val > 0:
            idx_rs = idx
            break
    return idx_rs

def error_check_for_matchings(assign_mat):
    high, width = assign_mat.shape
    row_zero_num = assign_mat.sum(axis=0).astype(int)
    col_zero_num = assign_mat.sum(axis=1).astype(int)

    rst = True
    for n in row_zero_num:
        if n > 1:
            rst = False
            break
    for n in col_zero_num:
        if n > 1:
            rst = False
            break

    if rst and high > 0 and width > 0:
        return rst
    else:
        return False

def step2(cost_mat):
    # print(cost_mat.shape[0], cost_mat.shape[1])
    high, width = cost_mat.shape
    mark_mat = np.zeros(cost_mat.shape).astype(int)
    row_mark = np.zeros(width, dtype=int)
    col_mark = np.zeros(high, dtype=int)

    zero_idxs = np.where(cost_mat==0)
    # print("zero_idxs:", zero_idxs[0], zero_idxs[1], type(zero_idxs[1]))

    for i, j in zip(zero_idxs[0], zero_idxs[1]):
        if (col_mark[i] == 0) and (row_mark[j] == 0):
            # starring
            mark_mat[i, j] = 1
            col_mark[i] = 1
            row_mark[j] = 1

    return mark_mat, row_mark, col_mark

def step4(zero_mat, mark_mat, row_cover, col_cover):
    rst = 0
    loop_cnt = 0
    while True:
        loop_cnt += 1

        zero_uncover = zero_mat.copy()
        row_idxs = np.where(col_cover==1)[0]
        col_idxs = np.where(row_cover==1)[0]
        # print(f"step4,{loop_cnt},row_idxs: ", row_idxs, type(row_idxs))
        # print(f"step4,{loop_cnt},col_idxs: ", col_idxs, type(col_idxs))
        zero_uncover[row_idxs, :] = 0
        zero_uncover[:, col_idxs] = 0
        # print(f"step4,{loop_cnt},zero_uncover:\r\n", zero_uncover)

        zero_idxs = np.where(zero_uncover==1)
        # print(f"step4,{loop_cnt},zero_idxs:", zero_idxs)

        if zero_idxs[0].size > 0:
            r, c = zero_idxs[0][0], zero_idxs[1][0]
            mark_mat[r, c] = 2
            # print(f"step4,{loop_cnt},mark_mat:\r\n", mark_mat)

            star_row = (mark_mat[r] == 1).astype(int)
            # print(f"step4,{loop_cnt},star_row:", star_row)

            star_idx = find_first_non_zero_item_idx(star_row)
            if star_idx is None:
                #step5
                rst = 5, r, c
                # print("rst:", rst, type(rst))
                break
            else:
                col_cover[r] = 1
                row_cover[star_idx] = 0
            
        else:
            # no uncovered zeros left
            # print(f"step4,{loop_cnt},no uncovered zeros left!")
            rst = 6
            break

    return rst
    
def step5(zero_mat, mark_mat, row_cover, col_cover, prime_pos):
    r, c = prime_pos
    aug_path = []
    while True:
        aug_path.append([r,c])
        star_col = (mark_mat[:, c] == 1).astype(int)
        star_idx = find_first_non_zero_item_idx(star_col)
        if star_idx is None:
            break

        aug_path.append([star_idx, c])
        r, c = star_idx, c

        prim_row = (mark_mat[star_idx] == 2).astype(int)
        prim_idx = find_first_non_zero_item_idx(prim_row)

        if star_idx is None:
            break

        r, c = r, prim_idx

    endn = aug_path[-1]

    if mark_mat[endn[0], endn[1]] != 2:
        print("error in step5, augment path is not found!, prime_pos:", prime_pos)
        return False

    # print("step5, aug_path:", aug_path)
    aug_path = tuple(zip(*aug_path))
    mark_mat[aug_path] = 3 - mark_mat[aug_path]
    # print("mark_mat: \r\n", mark_mat)
    mark_mat[mark_mat == 2] = 0
    # print("mark_mat: \r\n", mark_mat)
    return True

def step6(cost_mat, row_cover, col_cover):
    row_idxs = np.where(col_cover==0)[0]
    col_idxs = np.where(row_cover==0)[0]
    uncover_cost_mat = cost_mat[row_idxs, :]
    uncover_cost_mat = uncover_cost_mat[:, col_idxs]
    # # print("uncover_cost_mat: \r\n", uncover_cost_mat)
    minval = uncover_cost_mat.min()

    row_idxs = np.where(col_cover==1)[0]
    cost_mat[row_idxs, :] += minval
    cost_mat[:, col_idxs] -= minval

def MunkresAssign(cost_mat_org):
    cost_mat = cost_mat_org.copy()
    high, width = cost_mat.shape
    K = min(high, width)

    col_min = cost_mat.min(axis=1)
    # # print("col_min: ", col_min)
    cost_mat = cost_mat - col_min.reshape([-1,1])
    # print("cost_mat: \r\n", cost_mat)

    mark_mat, row_mark, col_mark = step2(cost_mat)
    # print("mark_mat:\r\n", mark_mat)
    # print("row_mark, col_mark:", row_mark, col_mark)

    i = 0
    while True:
        i += 1
        star_mark_mat = (mark_mat == 1).astype(int)
        # print(f"i{i}:star_mark_mat:\r\n", star_mark_mat)

        if not error_check_for_matchings(star_mark_mat):
            print(f"i{i}:error_check_for_matchings: have errors!")

        row_cover = star_mark_mat.sum(axis=0).astype(int)
        col_cover = np.zeros(col_mark.shape, dtype=int)

        if row_cover.sum() == K:
            # found a complete set of unigue assignments
            # print(f"i{i}:found a complete set of unigue assignments")
            break

        step4_cnt = 0
        while True:
            step4_cnt += 1
            zero_mat = (cost_mat == 0).astype(int)
            # print(f"step4,{step4_cnt},zero_mat:\r\n", zero_mat)
            rst_step = step4(zero_mat, mark_mat, row_cover, col_cover)
            # print(f"step4,{step4_cnt},rst_step:", rst_step, type(rst_step))
            # print(f"step4,{step4_cnt},mark_mat:\r\n", mark_mat)
            # print(f"step4,{step4_cnt},row_cover, col_cover:", row_cover, col_cover)

            if rst_step == 6:
                step6(cost_mat, row_cover, col_cover)
                # print(f"step4,{step4_cnt},cost_mat:\r\n", cost_mat)
            else:
                rst_step, r, c = rst_step
                bok = step5(zero_mat, mark_mat, row_cover, col_cover, (r, c))
                # print(f"step4,{step4_cnt},step5 return:", bok)
                break

    assign_result = cost_mat_org * mark_mat
    # print("assign_result:\r\n", assign_result, assign_result.sum())
    return assign_result.sum(), mark_mat


if __name__ == '__main__':
    for n in range(50):
        cost_mat = np.random.randint(1, high=1000, size=(9,10))
        print("cost_mat:\r\n", cost_mat)
        assign_result, assign_mat = MunkresAssign(cost_mat)
        
        high, width = cost_mat.shape
        # # print("assign_result:", assign_result, "\r\n", assign_mat)

        # check
        result_all = []
        perms = permutations(range(width), high)
        ## # print("perms:", perms)
        for i in perms:
            ## # print("assign:", list(range(high)), list(i), end=" ")
            assign = cost_mat[list(range(high)), list(i)]
            ## # print(assign)
            result_all.append(sum(assign))
        result_all.sort()
        print("result_all:", result_all[0:8], "...", result_all[-2:])
        if result_all[0] == assign_result:
            print(n+1, ": assign result is ok! minimum cost:", result_all[0], "\r\n", 
                    cost_mat[np.where(assign_mat==1)], np.where(assign_mat==1)[1])
        else:
            print("Error: result_all != assign_result:", result_all[0], assign_result)
        
