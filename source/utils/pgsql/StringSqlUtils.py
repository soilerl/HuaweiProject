


getAllUrls = "SELECT * FROM public.project_index"
#根据url获取指标
getIndexByUrl = "SELECT * FROM public.project_index WHERE url = '{url}'"

insertIndex = "INSERT INTO public.project_index(url, data) VALUES ('{url}', '{data}');"

updateIndex = "UPDATE public.project_index SET data='{data}' WHERE url = '{url}'"