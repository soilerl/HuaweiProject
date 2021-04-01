


getAllUrls = "SELECT * FROM public.project_index"
#根据url获取指标
getIndexByUrl = "SELECT * FROM public.project_index WHERE url = '{url}'"

insertIndex = "INSERT INTO public.project_index(url, data) VALUES ('{url}', '{data}');"

updateIndex = "UPDATE public.project_index SET data='{data}' WHERE url = '{url}'"

updateWeekDayMetric = """INSERT INTO public.codereview_week_per_day_metric(
	sunday, monday, tuesday, wednesday, thursday, friday, saturday, project_name, cal_time_range, created_at,
	 metric_name, project_id)
	VALUES ('{sunday}', '{monday}', '{tuesday}', '{wednesday}', '{thursday}', '{friday}', '{saturday}',
	 '{project_name}', '{cal_time_range}', '{created_at}', '{metric_name}', '{project_id}')"""

updateDayPerHourMetric = """INSERT INTO public.codereview_day_per_hour_metric(
	hour0, hour1, hour2, hour3, hour4, hour5, hour6, hour7, hour8, hour9, hour10, hour11, hour12, hour13, hour14, hour15, hour16, hour17, hour18, hour19, hour20, hour21, hour22, hour23, project_name, cal_time_range, metric_name, project_id, created_at)
	VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""


updateMonthMetric = """INSERT INTO public.codereview_month_metric(
	project_name, metric_name, cal_time_range, created_at, metric_time, metric_data, project_id)
	VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"""