
# coding: utf-8
from src.url_helper import *
from src.kick_parser import parse_commnunity_page
import pandas as pd
import zipfile
import json
from bs4 import BeautifulSoup
from datetime import datetime as dtm



def urls_to_srape_zip(zip_file):
    df_list = []
    with zipfile.ZipFile(zip_file, 'r') as f:
        for fn in f.namelist():
            df = pd.read_csv(f.open(fn))
            df = df[(df.state=='failed') | (df.state=='successful')]
            df['proj'] = df.urls.apply(lambda x: url_without_query_string(json.loads(x)['web']['project']))
            # df['update'] = df.proj.apply(lambda x: x+'/updates')
            # community page
            df['community'] = df.proj.apply(lambda x: x+'/community')
            df['proj_woeid'] = df.location.apply(lambda x: parse_url_qs(json.loads(x)['urls']['api']['nearby_projects'])['woe_id'][0] if not pd.isnull(x) else '')
            
            keep_cols = ['id', 'slug', 'community', 'proj_woeid']
            df_keep = df[keep_cols]
            df_list.append(df_keep)
            
    return pd.concat(df_list, ignore_index=True)
    

def scrape_woeid(projs_urls, headers_list, data_dir='data/scraped/patch-woeid/', save_step=5000, batch_cnt=0, debug=False, stop_batch=999999):
    """
    batch_cnt=0: start from No. batch_cnt, which means start from idx=batch_cnt*save_step. 
                           E.g. batch_cnt = 30, save_step=500 meaning it will start from idx=15000
    stop_batch=999999: stop before No. stop_batch, which means it stop when idx = stop_cnt*save_step 
                           (not including idx=stop_cnt*save step). 
                           E.g. stop_batch = 31, save step = 500, it will stop at idx=15500(the max idx scraped = 15499
    """
    errors = []
    batch_proj_ids = []
    batch_res_cities = []
    batch_res_countries = []
    error_file_name = data_dir + 'url_req_errors-{}_{}-{}.csv'
    batch_file_name_cities = data_dir + 'projs-back-cities-{}_{}-{}.csv'
    batch_file_name_countries = data_dir + 'projs-back-countries-{}_{}-{}.csv'

            
    def save_batch(batch_cnt, len_batch):
        # save parsed data in memory to disk
        start = batch_cnt * save_step
        end = start + len_batch - 1
        # save and clear errors
        df_errors = pd.DataFrame(errors, columns=['id','url', 'error'])
        df_errors.to_csv(error_file_name.format(start, end, batch_cnt), encoding='utf-8')
        del errors[:]
        # save and clear scraped result
        df_res = pd.DataFrame.from_dict(batch_res_cities)
        df_res.set_index('id').to_csv(batch_file_name_cities.format(start, end, batch_cnt), encoding='utf-8')
        del batch_res_cities[:]

        df_res = pd.DataFrame.from_dict(batch_res_countries)
        df_res.set_index('id').to_csv(batch_file_name_countries.format(start, end, batch_cnt), encoding='utf-8')
        del batch_res_countries[:]
        del batch_proj_ids[:]

    for idx, row in projs_urls.iterrows():
        # skip the first N batch
        if idx<batch_cnt*save_step:
            if idx==batch_cnt*save_step-1:
                print 'skip idx = %d and everything before it' % idx, dtm.now()
            continue
        # stop at some batch
        if idx>=stop_batch*save_step:
            print 'stop scraping before idx =', idx
            break
        proj_id = row['id']
        batch_proj_ids.append(proj_id)
        url = row.community

        html, error = req_html(proj_id, url, headers_list)
        if html:
            soup = BeautifulSoup(html)
            res = {}
            parse_commnunity_page(soup, res)
            if 'backer_cities' in res:
                for c in json.loads(res['backer_cities']):
                    c['id'] = proj_id
                    batch_res_cities.append(c)
            if 'backer_countries' in res:
                for c in json.loads(res['backer_countries']):
                    c['id'] = proj_id
                    batch_res_countries.append(c)
        else:
            errors.append(error)
            
        if (idx+1) % save_step == 0:
            print 'save %dth batch' % batch_cnt, 'each batch: %d rows' % save_step, dtm.now()
            save_batch(batch_cnt, len(batch_proj_ids))
            batch_cnt += 1
            
    # if there are scraped pages left
    if batch_proj_ids:
        print 'save last batch of %d rows' % len(batch_proj_ids), dtm.now()
        save_batch(batch_cnt, len(batch_proj_ids))


print 'prepare urls', dtm.now()
urls_df = urls_to_srape_zip('data/scraped/Kickstarter_2017-03-15T22_20_55_874Z.zip')
print 'saving woeid projects', dtm.now()
urls_df[['id', 'proj_woeid']].set_index('id').to_csv('data/projects_woeid.csv')

headers_list = get_headers_list()

print 'scraping'
scrape_woeid(urls_df, headers_list)