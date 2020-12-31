import os


from source.config.projectConfig import projectConfig

"""整个项目的工具类"""

#检测repo对应的mergeRequest是否存在，如果存在则删除
def mergeRequestFileExistAndDelete(repo=''):
    mergeRequestFileName = projectConfig.getMergeRequestDataPath() + os.sep + \
                           f"mergeRequest_{repo}.tsv"
    if os.path.exists(mergeRequestFileName):
        os.remove(mergeRequestFileName)

#检测repo对应的notes是否存在，如果存在则删除
def notesFileExistAndDelete(repo=''):
    notesFileName = projectConfig.getNotesDataPath() + os.sep + \
                                            f"notes_{repo}.tsv"
    if os.path.exists(notesFileName):
        os.remove(notesFileName)
#检测最终指标文件是否存在，如果存在则删除
def indexFileExistAndDelete():
    indexFileName = "project_index"
    if os.path.exists(indexFileName):
        os.remove(indexFileName)


#从url中获取仓库名
def getRepoFromUrl(url='') -> str:
    repoName = url.split('/')[-1]
    return repoName
#从url中获取owner
def getOwnerFromUrl(url='') -> str:
    owner = url.split('/')[-2]
    return owner
#根据owner和仓库名获取ProjectId
def getProjectIdByOwnerAndRepo(owner='', repoName=''):
    projectId = owner + r"%2F" + repoName
    return projectId



if __name__ == '__main__':
    print(getProjectIdByOwnerAndRepo("ss", "aa"))