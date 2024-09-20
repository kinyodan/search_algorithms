from typing import List, Tuple

class SegmentTreeSearch:
    def __init__(self, file_path: str, file_content: str):
        self.file_path = file_path
        self.file_content = file_content
        self.tree = []
        self.build_tree(sorted(self.file_content.split()))

    def build_tree(self, arr: List[str]):
        self.tree = [None] * (2 * len(arr))
        for i in range(len(arr)):
            self.tree[len(arr) + i] = arr[i]
        for i in range(len(arr) - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def search(self, target_string: str) -> Tuple[bool, str]:
        return self.segment_search(target_string, 0, len(self.tree) // 2 - 1, 1)

    def segment_search(self, target_string: str, l: int, r: int, pos: int) -> Tuple[bool, str]:
        if l == r:
            if self.tree[pos] == target_string:
                return True, self.tree[pos]
            return False, None
        mid = (l + r) // 2
        if target_string <= self.tree[2 * pos]:
            return self.segment_search(target_string, l, mid, 2 * pos)
        else:
            return self.segment_search(target_string, mid + 1, r, 2 * pos + 1)
