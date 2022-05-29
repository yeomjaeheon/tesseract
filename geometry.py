import numpy as np
import copy

def rot(tesseract, xy, xz, xw, yz, yw, zw): #라디안
    tesseract_modified = copy.deepcopy(tesseract)
    xy_rot_matrix = np.array([[np.cos(xy), -np.sin(xy), 0, 0], [np.sin(xy), np.cos(xy), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    xz_rot_matrix = np.array([[np.cos(xz), 0, -np.sin(xz), 0], [0, 1, 0, 0], [np.sin(xz), 0, np.cos(xz), 0], [0, 0, 0, 1]])
    xw_rot_matrix = np.array([[np.cos(xw), 0, 0, -np.sin(xw)], [0, 1, 0, 0], [0, 0, 1, 0], [np.sin(xw), 0, 0, np.cos(xw)]])
    yz_rot_matrix = np.array([[1, 0, 0, 0], [0, np.cos(yz), -np.sin(yz), 0], [0, np.sin(yz), np.cos(yz), 0], [0, 0, 0, 1]])
    yw_rot_matrix = np.array([[1, 0, 0, 0], [0, np.cos(yw), 0, -np.sin(yw)], [0, 0, 1, 0], [0, np.sin(yw), 0, np.cos(yw)]])
    zw_rot_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, np.cos(zw), -np.sin(zw)], [0, 0, np.sin(zw), np.cos(zw)]])

    rot_matrix = xy_rot_matrix
    for m in [xz_rot_matrix, xw_rot_matrix, yz_rot_matrix, yw_rot_matrix, zw_rot_matrix]:
        rot_matrix = np.dot(rot_matrix, m)

    for i in range(0, 2 ** tesseract.dimension):
        tesseract_modified.point_original[i] = np.dot(rot_matrix, tesseract.point_original[i] - tesseract.offset) + tesseract.offset

    return tesseract_modified

def proj(mode, tesseract, view_point):
    if mode == 1:
        proj_point = [tesseract.point_original[i][:2] * (view_point / (view_point + tesseract.point_original[i][2])) for i in range(0, 2 ** tesseract.dimension)]

    elif mode == 2:
        proj_point = [tesseract.point_original[i][:2] for i in range(0, 2 ** tesseract.dimension)]

    return proj_point

class tesseract:
    def __init__(self, x, y, z, w, size):
        self.dimension = 4

        self.size = size
        self.offset = np.array([x, y, z, w])

        self.point_original = [] #원형의 점을 기록
        self.lines = [] #원형의 연결관계를 기록

        tmp_point_basis = [] #변형 없는 점 기록
        tmp_point = np.array([-1, -1, -1, -1])

        for i in range(0, 2 ** self.dimension): # 정팔포체 원형의 점 생성
            tmp_point_basis.append(tmp_point * 1)

            tmp_carry = False #자리올림 여부
            tmp_index = 1 #자리올림이 일어날 경우 인덱스값으로 사용

            if tmp_point[0] == -1:
                tmp_point[0] = 1

            elif tmp_point[0] == 1:
                tmp_carry = True
                tmp_point[0] = -1

            while tmp_carry and tmp_index < self.dimension: #자리올림
                if tmp_point[tmp_index] == -1:
                    tmp_point[tmp_index] = 1
                    tmp_carry = False
                    break

                elif tmp_point[tmp_index] == 1:
                    tmp_point[tmp_index] = -1
                    tmp_carry = True

                tmp_index += 1

        for i in range(0, 2 ** self.dimension): #정팔포체 원형의 연결관계 저장
            for j in range(i + 1, 2 ** self.dimension):
                tmp_num_diff = np.sum((tmp_point_basis[i] != tmp_point_basis[j]).astype(np.int16)) #일치하는 성분의 개수 기록

                if tmp_num_diff == 1:
                    self.lines.append([i, j])

        for point in tmp_point_basis:
            self.point_original.append(point * self.size + self.offset)