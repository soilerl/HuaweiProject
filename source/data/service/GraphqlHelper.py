# coding=gbk
from source.utils.StringKeyUtils import StringKeyUtils
import json


class GraphqlHelper:
    """����graphql ��Ҫ��query���"""

    # @staticmethod
    # def getTimeLineQueryByNodes(body):
    #     """���ز�ѯtimeline��Ҫ�����"""
    #     body[StringKeyUtils.STR_KEY_QUERY] = GraphqlHelper.STR_KEY_QUERY_PR_TIMELINE
    #     return body

    @staticmethod
    def getGraphlQuery(body, query):
        """body ����query���"""
        if query is not None:
            body[StringKeyUtils.STR_KEY_QUERY] = query
        return body

    @staticmethod
    def getTimeLineQueryByNodes():
        """���ز�ѯtimeline��Ҫ�����"""
        return GraphqlHelper.STR_KEY_QUERY_PR_TIMELINE

    @staticmethod
    def getFollowingListByLoginFirst():
        return GraphqlHelper.STR_KEY_QUERY_FOLLOWING_LIST

    @staticmethod
    def getPrInformationByNumber():
        return GraphqlHelper.STR_KEY_QUERY_PR_ALL

    @staticmethod
    def getMrInformationByIID():
        return GraphqlHelper.STR_KEY_QUERY_MR_ALL

    @staticmethod
    def getTreeByOid():
        return GraphqlHelper.STR_KEY_QUERY_TREE

    @staticmethod
    def getGraphqlVariables(body, args=None):
        """���ش��ݲ�����Ҫ��json"""
        if args is None or isinstance(body, dict) is False:
            body[StringKeyUtils.STR_KEY_VARIABLES] = GraphqlHelper.STR_KEY_NONE
        else:
            body[StringKeyUtils.STR_KEY_VARIABLES] = json.dumps(args)
        return body

    # @staticmethod
    # def getGraphqlArg(args=None):
    #     """���ش��ݲ�����Ҫ��json"""
    #     pass

    STR_KEY_QUERY_VIEWER = "{viewer{name}}"

    STR_KEY_NONE = "{}"

    STR_KEY_QUERY_PR_TIMELINE = '''
query($ids:[ID!]!) { 
  nodes(ids:$ids) {
      ... on PullRequest {
      id
      author {
        login
      }
      timelineItems(first:100) {
        edges {
          node {
            __typename
            ... on Node {
               id
            }
              
            ... on PullRequestCommit {
              commit {
                oid
                authoredDate
                committedDate
                pushedDate
				author {
                  user {
                    login
                  }
                }
                message
              }
            }
            
            ... on PullRequestReview {
              commit {
                oid
              }
              author {
                login
              }
              bodyText
              createdAt
              comments(first: 100) {
                nodes {
                  commit {
                    oid
                    message
                  }
                  originalCommit {
                    oid
                    message
                  }
                  author {
                    login
                  }
                  path
                  createdAt
                }
              }
            }
            ... on HeadRefForcePushedEvent {
              afterCommit {
                oid
                message
              }
              beforeCommit {
                oid
                message
              }
              createdAt
            }
            ... on PullRequestReviewThread {
              id
              comments(first: 100) {
                nodes {
                  commit {
                    oid
                    message
                  }
                  originalCommit {
                    oid
                    message
                  }
                  author {
                    login
                  }
                  path
                  createdAt
                }
              }
            }
            ... on MergedEvent {
              id
              commit {
                oid
              }
              createdAt
            }
            ... on IssueComment {
              author {
                login
              }
              bodyText
              createdAt
            }
          }   
        }
        }
      }
    }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
    '''

    STR_KEY_QUERY_PR_ALL = '''query($name:String!, $owner:String!, $number:Int!) { 
      
      viewer {
       login
      }
	  
	  
      rateLimit {
        limit
        cost
        remaining
        resetAt
      }
	  
	  
      repository(name:$name, owner:$owner) { 
          issueOrPullRequest(number:$number) { 
           __typename
			 
			 
           ... on Issue {
              number
            }
			
			
           ... on PullRequest {
             # pull request����Ϣ  23
             # �� repo_full_name, comments
             # �� review_comments, commits
             # �� head, base
             
             number 
             databaseId
             id
             # id ��node id
             state
             title
             author {
               login
             }
             body
             createdAt
             updatedAt
             closedAt
             mergedAt
             mergeCommit {
               oid
             }
             authorAssociation
             merged
             additions
             deletions
             changedFiles
			 
			 
             #issue comment
             comments(first:50) {
              nodes {
               # 9�� �� repo_full_name,pull_number
                databaseId
                id
                author {
                  login
                }
                createdAt
                updatedAt
                authorAssociation
                body
              }
            }
			
			
            # review
            reviews(first:50) {
              nodes{
               # 11�� �� repo_full_name,pull_number,user_login
               databaseId
               author{
                 login
               }
               body
               state
               authorAssociation
               submittedAt
               commit {
                 oid
               }
               id
			  
			  # review comment ��Ƕ
              comments(first:50) {
                nodes {
                 # 21�� ��pull_request_review_id,
                 # startline,orignal_start_line,start_side,line,origin_line
                 # side
                 databaseId
                 author {
                   login
                 }
                 body
                 diffHunk
                 path
                 commit {
                   oid
                 }
                 position
                 originalPosition
                 originalCommit{
                   oid
                 }
                 createdAt
                 updatedAt
                 authorAssociation
                 replyTo {
                   databaseId
                 }
                 id
                }
              }
			  
			  
              # review �漰��commit
              commit {
                # 15������ ��status_total,commit_comment_count
                # commit_author_date, commit_committer_date
                oid
                id
                author {
                name
                email
                }
                committer {
                 name
                 email
                }
                tree {
                  id
                  oid
                }
                messageBody
                additions
                deletions
                changedFiles
                parents(first:50){
                  nodes {
                   oid
                  }
                 }
                }
			  
			  
              }
            }
			
			
            # user 
            participants(first:50){
            nodes {
               #����26�� �� type,followers_url,
               #following_url, starred_url, subscriptions_url,
               #organizations_url, repos_url, events_url
               #received_events_url, blog, public_repos,
               #public_gists, followers, following
               login
               isSiteAdmin
               databaseId
               email
               id
               name
               company
               location
               isHireable
               bio
               createdAt
               updatedAt
             }
            }
			
			
            #files
            files(first:50) {
               nodes {
               # ������ prֱ�ӹ������ļ��仯
               path
               additions
               deletions
               }
            }
			
			
            # pr ֱ����ص�commit
            commits(first:50) {
             nodes{
              commit {
              # 15������ ��status_total,commit_comment_count
              # commit_author_date, commit_committer_date
               oid
               id
               author {
                name
                email
               }
               committer {
                 name
                 email
                }
                tree {
                   oid
                   id
                }
                messageBody
                additions
                deletions
                changedFiles
                parents(first:50){
                  nodes {
                   oid
                  }
                }
              }
             }
            }
			
			
            # head branch
            headRef {
             name
             prefix
             id
             repository {
               name
               nameWithOwner
             }
            }
            headRefOid
            headRefName
            headRepository {
              name
              nameWithOwner
            }
			
			
            # base branch
            baseRef {
             name
             prefix
             id
             repository {
               name
               nameWithOwner
             }
            }
            baseRefOid
            baseRefName
            baseRepository {
              name
              nameWithOwner
            }
			
			
           }
        }  
      } 
    }'''

    STR_KEY_QUERY_TREE = """query($name:String!, $owner:String!, $expression:String, $oid:GitObjectID) { 
  repository(name:$name, owner:$owner) {
     object(expression:$expression, oid:$oid) {
        __typename
        ... on Blob {
        byteSize
        isBinary
        isTruncated
        text
        commitUrl
        commitResourcePath
        oid
        id
        repository {
          nameWithOwner
        }
     }

     ... on Tree {
        oid
        id
        entries {
          mode
          name
          type
          object {
            oid
            id
          }
        }
        repository {
          nameWithOwner
        }
     }

    }
  }
}"""

    STR_KEY_QUERY_FOLLOWING_LIST = """query($login:String!) { 
  user(login:$login) {
     name
     login
     following(first:100) {
       totalCount
       edges {
         cursor
         node {
            login 
            name
         }
       }
     }

     followers(first:100) {
       totalCount
       edges {
         cursor
         node {
            login 
            name
         }
       }
     }

     watching(first:100) {
       totalCount
       edges {
         cursor
         node {
           name
           nameWithOwner
         }
       }
     } 
  }
}"""

    STR_KEY_QUERY_MR_ALL = """query($project:ID!, $mr:String!) {
  project(fullPath: $project) {
     id
     mergeRequest(iid:$mr) {
      iid
      sourceBranch
      targetBranch
      mergeCommitSha
      diffStatsSummary {
          additions
          changes
          deletions
          fileCount
      }
      pipelines(first:100) {
        nodes {
          iid
          sha
          id
        }
      }
      discussions(first:100) {
        nodes {
          id
          notes(first:100) {
            nodes {
              id
              discussion {
                id
              }
            }
          }
        }
      } 
      notes(first:200) {
        nodes {
          createdAt
          id
          author {
            username
            name
          }
          system
          discussion {
            id
          }
          body
          position {
            diffRefs {
              baseSha
              headSha
              startSha
            }
            filePath
            newLine
            newPath
            oldLine
            oldPath
          }
        }
      }
    }
  }
}"""
