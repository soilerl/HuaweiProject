# coding=gbk


class StringKeyUtils:
    """�������ڴ������ʹ�õ�������key"""

    '''��Ŀ��Ϣʹ�õ�key
    '''
    STR_KEY_ID = 'id'
    STR_KEY_NUMBER = 'number'
    STR_KEY_LANG = 'language'
    STR_KEY_OWNER = 'owner'
    STR_KEY_LANG_OTHER = 'Other'
    STR_KEY_NODE_ID = 'node_id'
    STR_KEY_NAME = 'name'
    STR_KEY_FULL_NAME = 'full_name'
    STR_KEY_DESCRIPTION = 'description'
    STR_KEY_CREATE_AT = 'created_at'
    STR_KEY_CREATE_AT_V4 = 'createdAt'
    STR_KEY_UPDATE_AT = 'updated_at'
    STR_KEY_STARGAZERS_COUNT = 'stargazers_count'
    STR_KEY_WATCHERS_COUNT = 'watchers_count'
    STR_KEY_LANGUAGE = 'language'
    STR_KEY_FORKS_COUNT = 'forks_count'
    STR_KEY_SUBSCRIBERS_COUNT = 'subscribers_count'
    STR_KEY_OWNER_LOGIN = 'owner_login'
    STR_KEY_PARENT_FULL_NAME = 'parent_full_name'
    STR_KEY_PARENT = 'parent'

    '''�û���Ϣʹ�õ���key '''
    STR_KEY_LOGIN = 'login'
    STR_KEY_SITE_ADMIN = 'site_admin'
    STR_KEY_TYPE = 'type'
    STR_KEY_EMAIL = 'email'
    STR_KEY_FOLLOWERS_URL = 'followers_url'
    STR_KEY_FOLLOWING_URL = 'following_url'
    STR_KEY_STARRED_URL = 'starred_url'
    STR_KEY_SUBSCRIPTIONS_URL = 'subscriptions_url'
    STR_KEY_ORGANIZATIONS_URL = 'organizations_url'
    STR_KEY_REPOS_URL = 'repos_url'
    STR_KEY_EVENTS_URL = 'events_url'
    STR_KEY_RECEVIED_EVENTS_URL = 'received_events_url'
    STR_KEY_COMPANY = 'company'
    STR_KEY_BLOG = 'blog'
    STR_KEY_LOCATION = 'location'
    STR_KEY_HIREABLE = 'hireable'
    STR_KEY_BIO = 'bio'
    STR_KEY_PUBLIC_REPOS = 'public_repos'
    STR_KEY_PUBLIC_GISTS = 'public_gists'
    STR_KEY_FOLLOWERS = 'followers'
    STR_KEY_FOLLOWING = 'following'
    STR_KEY_PARTICIPANTS = 'participants'
    STR_KEY_SITE_ADMIN_V4 = 'isSiteAdmin'
    STR_KEY_HIREABLE_V4 = 'isHireable'
    STR_KEY_WATCHING = 'watching'

    '''pull request���ܻ�ʹ�õ�����Ϣ'''
    STR_KEY_STATE = 'state'
    STR_KEY_TITLE = 'title'
    STR_KEY_USER = 'user'
    STR_KEY_BODY = 'body'
    STR_KEY_CLOSED_AT = 'closed_at'
    STR_KEY_MERGED_AT = 'merged_at'
    STR_KEY_MERGE_COMMIT_SHA = 'merge_commit_sha'
    STR_KEY_AUTHOR_ASSOCIATION = 'author_association'
    STR_KEY_MERGED = 'merged'
    STR_KEY_COMMENTS = 'comments'
    STR_KEY_REVIEW_COMMENTS = 'review_comments'
    STR_KEY_COMMITS = 'commits'
    STR_KEY_ADDITIONS = 'additions'
    STR_KEY_DELETIONS = 'deletions'
    STR_KEY_CHANGED_FILES = 'changed_files'
    STR_KEY_HEAD = 'head'
    STR_KEY_BASE = 'base'
    STR_KEY_USER_ID = 'user_id'
    STR_KEY_BASE_LABEL = 'base_label'
    STR_KEY_HEAD_LABEL = 'head_label'
    STR_KEY_REPO_FULL_NAME = 'repo_full_name'
    STR_KEY_IS_PR = 'is_pr'
    STR_KEY_PULL_REQUEST = 'PullRequest'
    STR_KEY_ISSUE = 'Issue'
    STR_KEY_CREATE_AT_V4 = 'createdAt'
    STR_KEY_UPDATE_AT_V4 = 'updatedAt'
    STR_KEY_CLOSED_AT_V4 = 'closedAt'
    STR_KEY_MERGED_AT_V4 = 'mergedAt'
    STR_KEY_MERGE_COMMIT = 'mergeCommit'
    STR_KEY_AUTHOR_ASSOCIATION_V4 = 'authorAssociation'
    STR_KEY_REVIEWS = 'reviews'
    STR_KEY_CHANGED_FILES_V4 = 'changedFiles'
    STR_KEY_ISSUE_OR_PULL_REQUEST = 'issueOrPullRequest'
    STR_KEY_OPEN_V4 = 'OPEN'
    STR_KEY_CLOSED_V4 = 'CLOSED'
    STR_KEY_MERGED_V4 = 'MERGED'
    STR_KEY_OPEN_V3 = 'open'
    STR_KEY_CLOSED_V3 = 'closed'

    """gitlab MR�п��ܻ�ʹ�õ���key"""
    STR_KEY_IID = 'iid'
    STR_KEY_PROJECT_ID = 'project_id'
    STR_KEY_PROJECT = 'project'
    STR_KEY_MERGE_REQUEST_V4 = 'mergeRequest'
    STR_KEY_MERGED_BY = 'merged_by'
    STR_KEY_CLOSED_BY = 'closed_by'
    STR_KEY_TARGET_BRANCH = 'target_branch'
    STR_KEY_SOURCE_BRANCH = 'source_branch'
    STR_KEY_SOURCE_PROJECT_ID = 'source_project_id'
    STR_KEY_TARGET_PROJECT_ID = 'target_project_id'
    STR_KEY_SQUASH_COMMIT_SHA = 'squash_commit_sha'
    STR_KEY_CHANGES_COUNT = 'changes_count'
    STR_KEY_DIFF_REFS = 'diff_refs'
    STR_KEY_MERGED_BY_USER_NAME = 'merged_by_user_name'
    STR_KEY_CLOSED_BY_USER_NAME = 'closed_by_user_name'
    STR_KEY_AUTHOR_USER_NAME = 'author_user_name'
    STR_KEY_DIFF_REFS_V4 = 'diffRefs'
    STR_KEY_DIFF_STATUS_SUMMARY = 'diffStatsSummary'
    STR_KEY_FILE_COUNT_V4 = 'fileCount'
    STR_KEY_FILE_COUNT = 'file_count'

    """gitlab USER���ܻ��õ�"""
    STR_KEY_USER_NAME = 'username'
    STR_KEY_NOTEABLE_ID = 'noteable_id'
    STR_KEY_NOTEABLE_IID = 'noteable_iid'
    STR_KEY_NOTEABLE_TYPE = 'noteable_type'

    """gitlab refdifss���ܻ��õ�"""
    STR_KEY_BASE_SHA = 'base_sha'
    STR_KEY_HEAD_SHA = 'head_sha'
    STR_KEY_START_SHA = 'start_sha'
    STR_KEY_BASE_SHA_V4 = 'baseSha'
    STR_KEY_HEAD_SHA_V4 = 'headSha'
    STR_KEY_START_SHA_V4 = 'startSha'

    """gitlab pipeline���ܻ��õ�"""
    STR_KEY_MERGE_REQUEST_ID = 'merge_request_id'
    STR_KEY_PIPELINES_V4 = 'pipelines'

    """gitlab notes���ܻ��õ�"""
    STR_KEY_SYSTEM = 'system'
    STR_KEY_IS_SYSTEM = 'isSystem'

    """gitlab position���ܻ��õ�"""
    STR_KEY_NOTES_ID = 'notes_id'
    STR_KEY_NOTES_V4 = 'notes'
    STR_KEY_OLD_PATH = 'old_path'
    STR_KEY_NEW_PATH = 'new_path'
    STR_KEY_POSITION_TYPE = 'position_type'
    STR_KEY_OLD_LINE = 'old_line'
    STR_KEY_NEW_LINE = 'new_line'
    STR_KEY_OLD_PATH_V4 = 'oldPath'
    STR_KEY_NEW_PATH_V4 = 'newPath'
    STR_KEY_OLD_LINE_V4 = 'oldLine'
    STR_KEY_NEW_LINE_V4 = 'newLine'

    """gitlab diff���ܻ��õ�"""
    STR_KEY_NEW_FILE = 'new_file'
    STR_KEY_RENAMED_FILE = 'renamed_file'
    STR_KEY_DELETED_FILE = 'deleted_file'
    STR_KEY_DIFF = 'diff'
    STR_KEY_DIFFS = 'diffs'

    """gitlab discussion���ܻ��õ�"""
    STR_KEY_NOTES = 'notes'
    STR_KEY_DISCUSSIONS_V4 = 'discussions'
    STR_KEY_DISCUSSION_V4 = 'discussion'

    """gitlab Commits"""
    STR_KEY_SHORT_ID = 'short_id'
    STR_KEY_MESSAGE = 'message'
    STR_KEY_AUTHOR_NAME = 'author_name'
    STR_KEY_AUTHOR_EMAIL = 'author_email'
    STR_KEY_AUTHORED_DATE = 'authored_date'
    STR_KEY_COMMITTER_NAME = 'committer_name'
    STR_KEY_COMMITTER_EMAIL = 'committer_email'
    STR_KEY_COMMITTER_DATE = 'committer_date'
    STR_KEY_WEB_URL = 'web_url'
    STR_KEY_STATS_ADDITIONS = 'stats_additions'
    STR_KEY_STATS_DELETIONS = 'stats_deletions'
    STR_KEY_STATS_TOTAL = 'stats_total'
    STR_KEY_STATUS = 'status'
    STR_KEY_PARENT_IDS = 'parent_ids'

    '''Branch ���ܻ�ʹ�õ�����'''
    STR_KEY_LABEL = 'label'
    STR_KEY_REF = 'ref'
    STR_KEY_REPO = 'repo'
    STR_KEY_SHA = 'sha'
    STR_KEY_USER_LOGIN = 'user_login'
    STR_KEY_REPOSITORY = 'repository'
    STR_KEY_NAME_WITH_OWNER = 'nameWithOwner'
    STR_KEY_HEAD_REPOSITORY = 'headRepository'
    STR_KEY_BASE_REPOSITORY = 'baseRepository'
    STR_KEY_HEAD_REF_NAME = 'headRefName'
    STR_KEY_BASE_REF_NAME = 'baseRefName'
    STR_KEY_HEAD_REF_OID = 'headRefOid'
    STR_KEY_BASE_REF_OID = 'baseRefOid'

    '''review���ܻ�ʹ�÷�������'''
    STR_KEY_PULL_NUMBER = 'pull_number'
    STR_KEY_SUBMITTED_AT = 'submitted_at'
    STR_KEY_COMMIT_ID = 'commit_id'
    STR_KEY_SUBMITTED_AT_V4 = 'submittedAt'

    '''review comment ���ܻ��õ�������'''
    STR_KEY_PULL_REQUEST_REVIEW_ID = 'pull_request_review_id'
    STR_KEY_DIFF_HUNK = 'diff_hunk'
    STR_KEY_PATH = 'path'
    STR_KEY_POSITION = 'position'
    STR_KEY_ORIGINAL_POSITION = 'original_position'
    STR_KEY_ORIGINAL_COMMIT_ID = 'original_commit_id'
    STR_KEY_START_LINE = 'start_line'
    STR_KEY_ORIGINAL_START_LINE = 'original_start_line'
    STR_KEY_START_SIDE = 'start_side'
    STR_KEY_LINE = 'line'
    STR_KEY_ORIGINAL_LINE = 'original_line'
    STR_KEY_SIDE = 'side'
    STR_KEY_IN_REPLY_TO_ID = 'in_reply_to_id'
    STR_KEY_CHANGE_TRIGGER = 'change_trigger'
    STR_KEY_DIFF_HUNK_V4 = 'diffHunk'
    STR_KEY_ORIGINAL_POSITION_V4 = 'originalPosition'
    STR_KEY_ORIGINAL_COMMIT = 'originalCommit'
    STR_KEY_IN_REPLY_TO_ID_V4 = 'replyTo'
    STR_KEY_PULL_REQUEST_REVIEW_NODE_ID = 'pull_request_review_node_id'

    '''issue comment ���ܻ�ʹ�õ�����'''
    STR_KEY_BODY_V4 = 'bodyText'

    '''commit ���ܻ�ʹ�õ�����'''
    STR_KEY_COMMIT = 'commit'
    STR_KEY_AUTHOR = 'author'
    STR_KEY_DATE = 'date'
    STR_KEY_AUTHOR_LOGIN = 'author_login'
    STR_KEY_COMMITTER = 'committer'
    STR_KEY_COMMITTER_LOGIN = 'committer_login'
    STR_KEY_COMMIT_AUTHOR_DATE = 'commit_author_date'
    STR_KEY_COMMIT_COMMITTER_DATE = 'commit_committer_date'
    STR_KEY_MESSAGE = 'message'
    STR_KEY_COMMIT_MESSAGE = 'commit_message'
    STR_KEY_COMMENT_COUNT = 'comment_count'
    STR_KEY_COMMIT_COMMENT_COUNT = 'commit_comment_count'
    STR_KEY_STATS = 'stats'
    STR_KEY_STATUS = 'status'  # һ��ʹ����commitһ��ʹ����file
    STR_KEY_TOTAL = 'total'
    STR_KEY_STATUS_TOTAL = 'status_total'
    STR_KEY_STATUS_ADDITIONS = 'status_additions'
    STR_KEY_STATUS_DELETIONS = 'status_deletions'
    STR_KEY_PARENTS = 'parents'
    STR_KEY_FILES = 'files'
    STR_KEY_MESSAGE_BODY_V4 = 'messageBody'
    STR_KEY_COMMIT_AUTHOR_DATE_V4 = 'authoredDate'
    STR_KEY_COMMIT_COMMITTED_DATE_V4 = 'committedDate'
    STR_KEY_HAS_FILE_FETCHED = 'has_file_fetched'
    STR_KEY_TREE_OID = 'tree_oid'
    STR_KEY_TREE = 'tree'
    STR_KEY_BLOB = 'blob'

    '''file ���ܻ�ʹ�õ�����'''
    STR_KEY_COMMIT_SHA = 'commit_sha'
    STR_KEY_CHANGES = 'changes'
    STR_KEY_FILENAME = 'filename'
    STR_KEY_PATCH = 'patch'

    '''commit relation ����ʹ�õ�����'''
    STR_KEY_CHILD = 'child'

    '''���ô�����ܻ�ʹ�õ���key'''
    STR_PROXY_HTTP = 'http'
    STR_PROXY_HTTP_FORMAT = 'http://{}'

    '''column�����ο��ܻ�ʹ�õ���key'''
    STR_KEY_NOP = ''

    '''pr timelineItem ���ܻ�ʹ�õ���'''
    STR_KEY_PULL_REQUEST_NODE = 'pullrequest_node'
    STR_KEY_TIME_LINE_ITEM_NODE = 'timelineitem_node'
    STR_KEY_TIME_LINE_ITEMS = 'timelineItems'
    STR_KEY_EDGES = 'edges'
    STR_KEY_OID = 'oid'
    STR_KEY_ORIGIN = 'origin'
    STR_FAILED_FETCH = 'Failed to fetch'
    STR_KEY_PULL_REQUEST_REVIEW_THREAD = 'PullRequestReviewThread'

    '''review change relation ���ܻ��õ���'''
    STR_KEY_PULL_REQUEST_NODE_ID = 'pull_request_node_id'
    STR_KEY_REVIEW_NODE_ID = 'review_node_id'
    STR_KEY_CHANGE_NODE_ID = 'change_node_id'
    STR_KEY_REVIEW_POSITION = 'review_position'
    STR_KEY_CHANGE_POSITION = 'change_position'

    '''blob ���ܻ��õ�'''
    STR_KEY_BYTE_SIZE = 'byte_size'
    STR_KEY_BYTE_SIZE_V4 = 'byteSize'
    STR_KEY_IS_BINARY = 'is_binary'
    STR_KEY_IS_BINARY_V4 = 'isBinary'
    STR_KEY_IS_TRUNCATED = 'is_truncated'
    STR_KEY_IS_TRUNCATED_V4 = 'isTruncated'
    STR_KEY_TEXT = 'text'
    STR_KEY_OBJECT = 'object'

    '''TreeEntry ���ܻ��õ�'''
    STR_KEY_PARENT_OID = 'parent_oid'
    STR_KEY_CHILD_OID = 'child_oid'
    STR_KEY_PARENT_PATH = 'parent_path'
    STR_KEY_CHILD_PATH = 'child_path'
    STR_KEY_PARENT_TYPE = 'parent_type'
    STR_KEY_CHILD_TYPE = 'child_type'
    STR_KEY_ENTRIES = 'entries'
    STR_KEY_PARENT_NODE_ID = 'parent_node_id'
    STR_KEY_CHILD_NODE_ID = 'child_node_id'

    '''UserFollowRelation ���ܻ��õ�'''
    STR_KEY_FOLLOWING_LOGIN = 'following_login'
    STR_KEY_TOTAL_COUNT_V4 = 'totalCount'

    '''v4 �ӿڿ��ܻ��õ���'''
    STR_KEY_ERRORS = 'errors'
    STR_KEY_TYPE_NAME_JSON = '__typename'
    STR_KEY_EDGE = 'edge'
    STR_KEY_TYPE_NAME = 'typename'
    STR_KEY_DATA = 'data'
    STR_KEY_NODES = 'nodes'
    STR_KEY_NODE = 'node'
    STR_KEY_DATABASE_ID = 'databaseId'
    STR_KEY_CURSOR = 'cursor'

    STR_KEY_ERRORS_PR_NOT_FOUND = 'Could not resolve to an issue or pull request with the number of'

    '''HeadRefForcePushedEvent ���ܻ�ʹ�õ���'''
    STR_KEY_AFTER_COMMIT = 'afterCommit'
    STR_KEY_BEFORE_COMMIT = 'beforeCommit'
    STR_KEY_HEAD_REF_PUSHED_EVENT = 'HeadRefForcePushedEvent'

    '''PullRequestCommit ���ܻ�ʹ�õ���'''
    STR_KEY_PULL_REQUEST_COMMIT = 'PullRequestCommit'

    '''time line item ���ܻ���������������'''
    STR_KEY_ISSUE_COMMENT = 'IssueComment'
    STR_KEY_MENTIONED_EVENT = 'MentionedEvent'  # ���ἰ
    STR_KEY_SUBSCRIBED_EVENT = 'SubscribedEvent'  # �����¼�
    STR_KEY_PULL_REQUEST_REVIEW = 'PullRequestReview'
    STR_KEY_PULL_REQUEST_REVIEW_THREAD = 'PullRequestReviewThread'  # �൱��review
    STR_KEY_PULL_REQUEST_REVISION_MARKER = 'PullRequestRevisionMarker'
    STR_KEY_MERGED_EVENT = 'MergedEvent'
    STR_KEY_REFERENCED_EVENT = 'ReferencedEvent'  # commit���ã�һ�������merge������ǰ���������

    API_GITHUB = 'https://api.github.com'
    API_REVIEWS_FOR_PULL_REQUEST = '/repos/:owner/:repo/pulls/:pull_number/reviews'
    API_PULL_REQUEST_FOR_PROJECT = '/repos/:owner/:repo/pulls'
    API_COMMENTS_FOR_REVIEW = '/repos/:owner/:repo/pulls/:pull_number/reviews/:review_id/comments'
    API_COMMENTS_FOR_PULL_REQUEST = '/repos/:owner/:repo/pulls/:pull_number/comments'
    API_PULL_REQUEST = '/repos/:owner/:repo/pulls/:pull_number'
    API_PROJECT = '/repos/:owner/:repo'
    API_USER = '/users/:user'
    API_REVIEW = '/repos/:owner/:repo/pulls/:pull_number/reviews/:review_id'
    API_ISSUE_COMMENT_FOR_ISSUE = '/repos/:owner/:repo/issues/:issue_number/comments'
    API_COMMIT = '/repos/:owner/:repo/commits/:commit_sha'
    API_COMMITS_FOR_PULL_REQUEST = '/repos/:owner/:repo/pulls/:pull_number/commits'
    API_COMMIT_COMMENTS_FOR_COMMIT = '/repos/:owner/:repo/commits/:commit_sha/comments'
    API_COMMENT_FOR_REVIEW_SINGLE = '/repos/:owner/:repo/pulls/comments/:comment_id'
    API_GRAPHQL = '/graphql'

    """gitlab��api�ӿ�"""
    API_GITLAB = 'https://gitlab.com/api/v4'
    API_GITLAB_GRAPHQL = 'https://gitlab.com/api/graphql'
    API_GITLAB_MERGE_PULL_REQUEST = '/projects/:id/merge_requests/:merge_request_iid'
    API_GITLAB_NOTES = '/projects/:id/merge_requests/:merge_request_iid/notes'
    API_GITLAB_COMMITS = '/projects/:id/merge_requests/:merge_request_iid/commits'
    API_GITLAB_COMMITS_COMPARE = '/projects/:id/repository/compare'

    # �����滻���ַ���
    STR_HEADER_PRIVATE_TOKEN = 'PRIVATE-TOKEN'
    STR_HEADER_AUTHORIZAITON = 'Authorization'
    STR_HEADER_TOKEN = 'token '  # �пո�
    STR_HEADER_BEARER = 'Bearer '  # �пո�
    STR_HEADER_ACCEPT = 'Accept'
    STR_HEADER_CONTENT_TYPE = 'content-type'
    STR_HEADER_MEDIA_TYPE = 'application/vnd.github.comfort-fade-preview+json'
    STR_HEADER_APPLICATION = 'application/json'
    STR_HEADER_RATE_LIMIT_REMIAN = 'X-RateLimit-Remaining'
    STR_HEADER_RATE_LIMIT_RESET = 'X-RateLimit-Reset'
    STR_HEADER_USER_AGENT = 'User-Agent'
    STR_HEADER_USER_AGENT_SET = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]

    STR_OWNER = ':owner'
    STR_REPO = ':repo'
    STR_PULL_NUMBER = ':pull_number'
    STR_REVIEW_ID = ':review_id'
    STR_USER = ':user'
    STR_ISSUE_NUMBER = ':issue_number'
    STR_COMMIT_SHA = ':commit_sha'
    STR_COMMENT_ID = ':comment_id'
    STR_GITLAB_REPO_ID = ':id'
    STR_GITLAB_MR_NUMBER = ':merge_request_iid'

    STR_PARM_STARE = 'state'
    STR_PARM_ALL = 'all'
    STR_PARM_OPEN = 'open'
    STR_PARM_CLOSED = 'closed'

    RATE_LIMIT = 5
    API_VERSION_RESET = 3
    API_VERSION_GRAPHQL = 4

    """json 404�����õ���"""
    STR_NOT_FIND = 'Not Found'

    """����ת���õ���"""
    STR_STYLE_DATA_DATE = '%Y-%m-%dT%H:%M:%SZ'

    """tsv �ļ�ʹ�õ���"""
    STR_SPLIT_SEP_TSV = '\t'

    """csv �ļ�ʹ�õ���"""
    STR_SPLIT_SEP_CSV = ','

    """��·���ָ������Ҫ��"""
    STR_SPLIT_SEP_ONE = '\\'
    STR_SPLIT_SEP_TWO = '/'

    """graphql �����õ���"""
    STR_KEY_QUERY = 'query'
    STR_KEY_OPERATIONAME = 'operationName'
    STR_KEY_VARIABLES = 'variables'

    """����ѧϰ����ʶʹ�õ�"""
    STR_ALGORITHM_FPS = 'fps'
    STR_ALGORITHM_NB = 'naiveBayes'
    STR_ALGORITHM_SVM = 'svm'
    STR_ALGORITHM_DT = 'decisionTree'
    STR_ALGORITHM_RF = 'randomForest'
    STR_ALGORITHM_IR = 'ir'
    STR_ALGORITHM_CN = 'cn'
    STR_ALGORITHM_CF = 'cf'

    """���ǩ"""
    STR_ALGORITHM_DT_M = 'decisionTree_m'
    STR_ALGORITHM_RF_M = 'randomForest_m'
    STR_ALGORITHM_ET_M = 'extraTree_m'
    STR_ALGORITHM_ETS_M = 'extraTrees_m'
    STR_ALGORITHM_TC = 'tc'
    STR_ALGORITHM_PB = 'pb'

    """issue comment �� review comment ��ǩ������"""
    STR_LABEL_ISSUE_COMMENT = 'label_issue_comment'
    STR_LABEL_REVIEW_COMMENT = 'label_review_comment'
    STR_LABEL_ALL_COMMENT = 'label_all_comment'

    """������ʶ���������"""
    STR_NAME_BOT = '[bot]'

    """��ʶ��ͬ��ѵ����ʽ"""
    STR_TEST_TYPE_SLIDE = 'test_type_slide'
    STR_TEST_TYPE_INCREMENT = 'test_type_increment'

    """��Ա������"""
    STR_USER_NONE = 'user_for_none'

    """�ؼ�����ȡ����"""
    STR_ALGORITHM_HYPER_GRAPH = 'hyper_graph'
    STR_ALGORITHM_ATF_PDF = 'atf_pdf'
