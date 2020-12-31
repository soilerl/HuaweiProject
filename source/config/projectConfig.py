# _*_ coding: utf-8 _*_
import os


class projectConfig:
    # projectName = 'NJU_HUAWEI'
    projectName = 'HuaweiProject'
    PATH_CONFIG = 'source' + os.sep + 'config' + os.sep + 'config.txt'
    # PATH_CONFIG = os.sep + 'config.txt'
    PATH_TEST_INPUT_EXCEL = 'data' + os.sep + 'Test200.xlsx'
    PATH_TEST_OUTPUT_EXCEL = 'data' + os.sep + 'output.xlsx'
    PATH_TEST_OUTPUT_PATH = 'data'
    PATH_STOP_WORD_HGD = 'data' + os.sep + 'HGDStopWord.txt'
    PATH_SPLIT_WORD_EXCEL = 'data' + os.sep + 'output_splitword.xlsx'
    PATH_USER_DICT_PATH = 'data' + os.sep + 'user_dict.utf8'
    PATH_TEST_CRF_INPUT = 'data' + os.sep + 'people-daily.txt'
    PATH_TEST_CRF_TEST_RESULT = 'data' + os.sep + 'test.rst'
    PATH_TEST_REVIEW_COMMENT = 'data' + os.sep + 'reviewComments.tsv'
    PATH_TEST_WINE_RED = 'data' + os.sep + 'winequality-red.xlsx'
    PATH_TEST_REVHELPER_DATA = 'data' + os.sep + 'revhelperDemoData.csv'
    PATH_TEST_FPS_DATA = 'data' + os.sep + 'FPSDemoData.tsv'
    PATH_STOP_WORD_ENGLISH = 'data' + os.sep + 'stop-words_english_1_en.txt'
    PATH_RUBY_KEY_WORD = 'data' + os.sep + 'rubyKeyWord.txt'
    PATH_CHANGE_TRIGGER = 'data' + os.sep + 'pullrequest_rails.tsv'
    PATH_COMMIT_RELATION = 'data' + os.sep + 'train' + os.sep + 'prCommitRelation'
    PATH_ISSUE_COMMENT_PATH = 'data' + os.sep + 'train' + os.sep + 'issueCommentData'
    PATH_DATA_TRAIN = 'data' + os.sep + 'train'
    PATH_COMMIT_FILE = 'data' + os.sep + 'train' + os.sep + 'commitFileData'
    PATH_SEAA = 'data' + os.sep + 'SEAA'
    PATH_PULL_REQUEST = 'data' + os.sep + 'train' + os.sep + 'pullRequestData'
    PATH_PR_CHANGE_FILE = 'data' + os.sep + 'train' + os.sep + 'prChangeFile'
    PATH_REVIEW = 'data' + os.sep + 'train' + os.sep + 'reviewData'
    PATH_TIMELINE = 'data' + os.sep + 'train' + os.sep + 'prTimeLineData'
    PATH_REVIEW_COMMENT = 'data' + os.sep + 'train' + os.sep + 'reviewCommentData'
    PATH_REVIEW_CHANGE = 'data' + os.sep + 'train' + os.sep + 'reviewChangeData'
    PATH_PULL_REQUEST_DISTANCE = 'data' + os.sep + 'train' + os.sep + 'prDistance'
    PATH_USER_FOLLOW_RELATION = 'data' + os.sep + 'train' + os.sep + 'userFollowRelation'
    PATH_USER_WATCH_REPO_RELATION = 'data' + os.sep + 'train' + os.sep + 'userWatchRepoRelation'
    PATH_STOP_WORD_STEM = 'data' + os.sep + 'stemStopWord.txt'
    PATH_COMMENT_KEY_WORD = 'data' + os.sep + 'train' + os.sep + 'commentKeyWord'

    PATH_DATA_MERGE_REQUEST = 'data' + os.sep + 'file' + os.sep + 'mergeRequest'
    PATH_DATA_NOTES = 'data' + os.sep + 'file' + os.sep + 'notes'

    TEST_OUT_PUT_SHEET_NAME = 'sheet1'

    @staticmethod
    def getRootPath():
        curPath = os.path.abspath(os.path.dirname(__file__))
        # print(curPath)
        projectName = projectConfig.projectName
        rootPath = os.path.join(curPath.split(projectName)[0], projectName)  # 获取myProject，也就是项目的根路径
        return rootPath


    @staticmethod
    def getConfigPath():
        rootPath = projectConfig.getRootPath()
        filePath = projectConfig.PATH_CONFIG
        # path = rootPath + filePath
        return os.path.join(rootPath, filePath)

    @staticmethod
    def getDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_OUTPUT_PATH)

    @staticmethod
    def getTestInputExcelPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_INPUT_EXCEL)

    @staticmethod
    def getTestoutputExcelPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_OUTPUT_EXCEL)

    @staticmethod
    def getStopWordHGDPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_STOP_WORD_HGD)

    @staticmethod
    def getSplitWordExcelPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_SPLIT_WORD_EXCEL)

    @staticmethod
    def getStopWordStemPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_STOP_WORD_STEM)

    @staticmethod
    def getCommentKeyWordPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_COMMENT_KEY_WORD)

    @staticmethod
    def getMergeRequestDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_DATA_MERGE_REQUEST)

    @staticmethod
    def getNotesDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_DATA_NOTES)



