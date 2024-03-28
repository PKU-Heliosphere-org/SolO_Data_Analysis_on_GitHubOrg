import requests
from bs4 import BeautifulSoup
import datetime
import julian


def get_archive_url(time_range,image_level):
    begin_datetime = time_range[0]
    end_datetime = time_range[1]

    delta_days = (end_datetime - begin_datetime).days
    begin_year = begin_datetime.year
    begin_month = begin_datetime.month
    begin_day = begin_datetime.day

    archive_url_list = []
    for i in range(delta_days + 1):
        archive_url = "https://sidc.be/EUI/data/"+image_level+"/" +'{:04d}/{:02d}/{:02d}/'.format(begin_year,begin_month,begin_day+i) 
        archive_url_list.append(archive_url)
    return archive_url_list

def get_files_links(archive_url):
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content,features="lxml")
    links = soup.findAll('a')
    file_links = [archive_url + link['href'] for link in links if link['href'].endswith('fits') or link['href'].endswith('jp2')] #后缀名: .jp2
    return file_links

def check_if_file_datetime_in_time_range(file_datetime, time_range):
    file_julian_time = julian.to_jd(file_datetime)
    begin_julian_time_range = julian.to_jd(time_range[0])
    end_julian_time_range = julian.to_jd(time_range[1])

    if (file_julian_time >= begin_julian_time_range) and (file_julian_time <= end_julian_time_range):
        is_in_timerange = True
    else:
        is_in_timerange = False

    return is_in_timerange

def download_file_series(time_range, image_type='fsi174',image_level='L3', local_dir='./'):

    archive_url_list = get_archive_url(time_range, image_level)

    downloaded_file_list = []

    for archive_url in archive_url_list:

        file_links = get_files_links(archive_url)

        for link in file_links:

            file_name = link.split('/')[-1]
            file_type = file_name.split('_')[2]
            file_time_str = file_name.split('_')[3]
            file_datetime = datetime.datetime.strptime(file_time_str, "%Y%m%dT%H%M%S%f")
            is_in_timerange = check_if_file_datetime_in_time_range(file_datetime, time_range)

            if file_type == ('eui-'+image_type+'-image') and is_in_timerange:
                print("Downloading file:%s" % file_name)
                r = requests.get(link, stream=True)
            # download starts
                with open(local_dir+file_name, 'wb') as f:
                    for chunk in r.iter_content():
                            f.write(chunk)
                downloaded_file_list.append(local_dir+file_name)
                print("%s downloaded!\n" % file_name)
            else:
                continue
    if downloaded_file_list:
        print("All files downloaded!")
    if not downloaded_file_list:
        print("Failed downloading EUI" +image_type+ " maps")

    return downloaded_file_list

