
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
#cost_mat = np.random.randint(1, high=1000, size=(10,10))
#print("cost_mat:\r\n", cost_mat)

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

def find_min_non_zero_item_idx(vector):
    idx_rs = None
    val_min = 0
    for idx, val in enumerate(vector):
        if val > 0:
            if (val_min == 0) or (val < val_min):
                val_min = val
                idx_rs = idx
            
    return idx_rs

def find_first_non_zero_num_idx(zero_num, zero_num_sort):
    idx_rs = None
    for idx in zero_num_sort:
        if zero_num[idx] > 0:
            idx_rs = idx
            break
    return idx_rs



def find_t0(zero_mark_mat):
    row_zero_num = zero_mark_mat.sum(axis=0)
    # print("row_zero_num: ", row_zero_num)
    col_zero_num = zero_mark_mat.sum(axis=1)
    # print("col_zero_num: ", col_zero_num)

    zero_num = np.append(col_zero_num,row_zero_num)
    # print("zero_num: ", zero_num)
    zero_num_sort = np.argsort(zero_num)
    # print("zero_num_sort: ", zero_num_sort)

    zero_num_idx = find_first_non_zero_num_idx(zero_num, zero_num_sort)
    # print("zero_num_idx: ", zero_num_idx)

    if zero_num_idx is None:
        return None

    high, width = zero_mark_mat.shape

    if zero_num_idx < high:
        # 
        if col_zero_num[zero_num_idx] == 1:
            # print("zero_mark_mat[zero_num_idx, :]: ", zero_mark_mat[zero_num_idx, :])
            col_pos = find_first_non_zero_item_idx(zero_mark_mat[zero_num_idx, :])
            # print("col_pos: ", col_pos)
        else:
            # print("zero_mark_mat[zero_num_idx, :] * row_zero_num: ", zero_mark_mat[zero_num_idx, :] * row_zero_num)
            col_pos = find_min_non_zero_item_idx(zero_mark_mat[zero_num_idx, :] * row_zero_num)
            # print("col_pos: ", col_pos)
        return zero_num_idx, col_pos
    else:
        zero_num_idx -= high
        if row_zero_num[zero_num_idx] == 1:
            # print("zero_mark_mat[:, zero_num_idx]: ", zero_mark_mat[:, zero_num_idx])
            row_pos = find_first_non_zero_item_idx(zero_mark_mat[:, zero_num_idx])
            # print("row_pos: ", row_pos)
        else:
            # print("zero_mark_mat[:, zero_num_idx] * col_zero_num: ", zero_mark_mat[:, zero_num_idx] * col_zero_num)
            row_pos = find_min_non_zero_item_idx(zero_mark_mat[:, zero_num_idx] * col_zero_num)
            # print("row_pos: ", row_pos)
        return row_pos, zero_num_idx

def is_perfect_matchings(assign_mat):
    high, width = assign_mat.shape
    row_zero_num = assign_mat.sum(axis=0).astype(int)
    col_zero_num = assign_mat.sum(axis=1).astype(int)

    rst = True
    for n in row_zero_num:
        if n != 1:
            rst = False
            break
    for n in col_zero_num:
        if n != 1:
            rst = False
            break

    if rst and high > 0 and width > 0:
        return rst
    else:
        return False

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


def mark_for_line_cover(zero_mark_mat, assign_mat):
    # print("zero_mark_mat: \r\n", zero_mark_mat)
    # print("assign_mat: \r\n", assign_mat)
    #
    high, width = cost_mat.shape
    col_mark = np.zeros((high,),dtype = int)
    row_mark = np.zeros((width,),dtype = int)

    row_idxs = []
    col_assign_num = assign_mat.sum(axis=1)
    for idx, val in enumerate(col_assign_num):
        if val == 0:
            col_mark[idx] = 1
            row_idxs.append(idx)

    while row_idxs:
        row_idx = row_idxs.pop(0)
        for i, val in enumerate(zero_mark_mat[row_idx, :]):
            if val == 1:
                if assign_mat[row_idx, i] == 0:
                    if row_mark[i] == 0:
                        row_mark[i] = 1
                        t0_idx = find_first_non_zero_item_idx(assign_mat[:, i])
                        if t0_idx != None:
                            if col_mark[t0_idx] == 0:
                                col_mark[t0_idx] = 1
                                row_idxs.append(t0_idx)

    return row_mark, col_mark

def line_cover(cost_mat, row_mark, col_mark):
    high, width = cost_mat.shape
    row_idxs = np.where(col_mark==1)[0]
    col_idxs = np.where(row_mark==0)[0]
    # print("row_idxs: ", row_idxs, type(row_idxs))
    # print("col_idxs: ", col_idxs, type(col_idxs))
    uncover_cost_mat = cost_mat[row_idxs, :]
    uncover_cost_mat = uncover_cost_mat[:, col_idxs]
    # print("uncover_cost_mat: \r\n", uncover_cost_mat)
    minval = uncover_cost_mat.min()
    cost_mat[row_idxs, :] -= minval
    col_idxs = np.where(row_mark==1)[0]
    cost_mat[:, col_idxs] += minval

def HungarianAlgorithms(cost_mat_org):
    cost_mat = cost_mat_org.copy()
    
    high, width = cost_mat.shape
    assign_mat = np.zeros(cost_mat.shape).astype(int)
    # print(cost_mat.shape[0], cost_mat.shape[1])

    row_min = cost_mat.min(axis=0)
    # print("row_min: ", row_min)

    cost_mat = cost_mat - row_min
    # print("cost_mat: \r\n", cost_mat)

    col_min = cost_mat.min(axis=1)
    # print("col_min: ", col_min)

    cost_mat = cost_mat - col_min.reshape([-1,1])
    # print("cost_mat: \r\n", cost_mat)

    ii = 0
    while True:
        zero_mark_mat = (cost_mat == 0).astype(int)
        # print("zero_mark_mat: \r\n", zero_mark_mat)
        zero_mark_mat_bak = zero_mark_mat.copy()

        t0_pos = find_t0(zero_mark_mat)
        # print("t0_pos:", t0_pos)

        i = 0
        while True:
            if t0_pos:
                assign_mat[t0_pos] = 1
                # print(f"{i}. assign_mat: \r\n", assign_mat)
                zero_mark_mat[t0_pos[0], :] = 0
                zero_mark_mat[:, t0_pos[1]] = 0
                # print(f"{i}. zero_mark_mat: \r\n", zero_mark_mat)
            else:
                break

            t0_pos = find_t0(zero_mark_mat)
            # print("t0_pos:", t0_pos)
            i+=1

        if not error_check_for_matchings(assign_mat):
            print("error_check_for_matchings: have errors!")
        else:
            # print("error_check_for_matchings: no errors!")
            pass

        is_ok = is_perfect_matchings(assign_mat)
        if is_ok:
            # print("perfect_matchings is found! assign_mat")
            break
        else:
            #print("the assign_mat is not perfect_matchings!")
            pass

            row_mark, col_mark = mark_for_line_cover(zero_mark_mat_bak, assign_mat)
            # print("row_mark: ", row_mark)
            # print("col_mark: ", col_mark)

            # print("cost_mat: \r\n", cost_mat)
            line_cover(cost_mat, row_mark, col_mark)
            # print("cost_mat: \r\n", cost_mat)
            assign_mat[:,:] = 0
        ii+=1
    assign_result = cost_mat_org * assign_mat
    return assign_result.sum(), assign_mat


if __name__ == '__main__':
    for n in range(10):
        cost_mat = np.random.randint(1, high=1000, size=(10,10))
        print("cost_mat:\r\n", cost_mat)
        assign_result, assign_mat = HungarianAlgorithms(cost_mat)
        
        high, width = cost_mat.shape
        # print("assign_result:", assign_result, "\r\n", assign_mat)

        # check
        result_all = []
        perms = permutations(range(width))
        ## print("perms:", perms)
        for i in perms:
            ## print("assign:", list(range(high)), list(i), end=" ")
            assign = cost_mat[list(range(high)), list(i)]
            ## print(assign)
            result_all.append(sum(assign))
        result_all.sort()
        # print("result_all:", result_all[0:8], "...", result_all[-2:])
        if result_all[0] == assign_result:
            print(n+1, "result is ok!", result_all[0], "\r\n", 
                    cost_mat[np.where(assign_mat==1)], np.where(assign_mat==1)[1])
        else:
            print("Error: result_all != assign_result:", result_all[0], assign_result)


 

