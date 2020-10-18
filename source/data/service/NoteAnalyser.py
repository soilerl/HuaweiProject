#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/15 22:54
# @Author : NJU
# @Version：V 0.1
# @File : NoteAnalyser.py
# @desc :
import re

from source.data.bean.Notes import Notes


class NoteAnalyser:
    """对于gitlab的某些活动 没有字段可以直接区分
       通过解析body来分析什么类型

       现在可识别类型：

       Commit提交：
           字段识别：无 position, system = True

           单个commit body实例：
           "added 1 commit\n\n<ul><li>c867db91 - Add documentation for incrementally expand mr diffs</li></ul>\n\n
           [Compare with previous version](/gitlab-org/gitlab-ce/merge_requests/31878/diffs?diff_id=51771304
           &start_sha=070b82270658e4bfee0a36f5570645b8e0f84e93)"

           多个commit body实例1：
            "added 27 commits\n\n<ul><li>5f6c4679...a039d6e0 - 23 commits from branch <code>tezos:master</code></li><li>
            9284cc80 - Bin_validation: main entry point in the monad</li><li>e57bfd12 -
            Bin_validation: reorder request matching</li><li>a030d601 -
            Bin_validation: be more obvious about recursion</li><li>267f6031 -
            Node/Validation: proper exit wrapping of validation process</li>
            </ul>\n\n[Compare with previous version](/tezos/tezos/-/merge_requests/2093/diffs?diff_id=116454457&
            start_sha=5f6c4679c2d1efacc342262d424e328d148f25e6)"

            多个commit body实例2：
            "added 3 commits\n\n<ul><li>06c3c5db - Test Michelson: check an error is raise if the same field is duplicated
            </li><li>73706166 - Test: add tests verifying missing fields are handled correctly</li><li>a6112411 - 
            Rename namespace in field</li></ul>\n\n[Compare with previous version]
            (/tezos/tezos/-/merge_requests/2125/diffs?diff_id=115591995&start_sha=923885c661c88def34a73f3ccc2e32c189156047)"

       代码评审:
            字段识别： 存在position, system = False

       讨论（Discussion）中的系统消息:
            字段识别： 存在position, system = True

            系统消息实例：changed this line in [version 12 of the diff]
            (/tezos/tezos/-/merge_requests/2093/diffs?diff_id=113335855&
            start_sha=1582beb8de02e87eb395cf0c3d15a676e119600d#4a1c785da64211105c485358b458327966ca1bc3_59_59)
    """

    @staticmethod
    def analysisSingleNote(note):
        """分析单个note可能的类型"""
        if isinstance(note, Notes):
            if note.position is None:
                """如果不存在position"""
                if note.system:
                    isCommit, shas = NoteAnalyser.recognizeCommitBody(note.body)
                    if not isCommit:
                        note.notesType = Notes.STR_KEY_OTHER
                    else:
                        """若为 commit， 识别最后一个commit作为修改的最后版本"""
                        note.notesType = Notes.STR_KEY_COMMIT
                        note.commit_sha = shas[-1]
                else:
                    note.notesType = Notes.STR_KEY_OTHER
            else:
                if note.system:
                    """说明是系统判断触发变更的状况"""
                    note.notesType = Notes.STR_KEY_SYSTEM_CHANGE_NOTICE
                else:
                    """说明是正常的代码评审"""
                    note.notesType = Notes.STR_KEY_INLINE_COMMENT

    @staticmethod
    def recognizeCommitBody(body):
        tempBody = body
        """尝试使用正则表达式来判断是否是commit提交类型
           标识特征  added x commit
           主要识别长度为6位的commit sha
           返回类型   (True, [sha1, sha2, ...])  第一位用于判断是否是commit，第二部分返回识别出来的sha

           """
        str_commit = r'^added \d* commit'  # 坑 中间的是空格，而不是 \xa0
        commit_pattern = re.compile(str_commit)
        result = commit_pattern.match(tempBody)
        if result is None:
            return False, []
        else:
            """可能需要处理rebase引入的commit，感觉暂时不处理问题也不算大"""
            commit_sha_pattern = re.compile(r'<li>[0-9a-f]{8}')
            commits = [x[4:] for x in commit_sha_pattern.findall(body)]
            return True, commits

if __name__ == "__main__":
    body = "added 12 commits\n\n<ul><li>a4ee65d0...43e8b13f - 10 commits from branch <code>tezos:master</code></li><li>524a8170 - Bin_validation: main entry point in the monad</li><li>3e6e38cd - Node/Validation: proper exit wrapping of validation process</li></ul>\n\n[Compare with previous version](/tezos/tezos/-/merge_requests/2093/diffs?diff_id=112623045&start_sha=a4ee65d0e5657d173aaeacc74a36e1f450ca692e"
    body1 = """added 27 commits

<ul><li>5f6c4679...a039d6e0 - 23 commits from branch <code>tezos:master</code></li><li>9284cc80 - Bin_validation: main entry point in the monad</li><li>e57bfd12 - Bin_validation: reorder request matching</li><li>a030d601 - Bin_validation: be more obvious about recursion</li><li>267f6031 - Node/Validation: proper exit wrapping of validation process</li></ul>

[Compare with previous version](/tezos/tezos/-/merge_requests/2093/diffs?diff_id=116454457&start_sha=5f6c4679c2d1efacc342262d424e328d148f25e6)"""
    NoteAnalyser.recognizeCommitBody(body)



