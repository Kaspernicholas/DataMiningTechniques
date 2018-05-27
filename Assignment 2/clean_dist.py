import pandas as pd
import numpy as np
from math import isnan

FILE_FULL = './data/training_set_VU_DM_2014.csv'

if __name__ == '__main__':
    print('--- Starting Data Cleanup ---')

    #data = pd.read_csv(FILE)

    print('Loading Full Dataset...')
    data_full = pd.read_csv(FILE_FULL)
    print('Loaded')

    # clean up orig_destination_distance attribute

    for i in range(0, 20):
        print('Cleaning File {}'.format(i))
        data = pd.read_csv('./data/train_split_cleaned2/train_data_{:02d}.csv'.format(i))
        data.drop(columns=['Unnamed: 0'], inplace=True)
        data['avg_orig_dist'] = 0
        data['std_orig_dist'] = 0

        s_ids = data['srch_id'].unique()
        for j, s_id in enumerate(s_ids):
            #print('Search ID {}  |  {}/{}'.format(s_id, j, len(s_ids)))
            # get block of each search
            search = data.loc[data['srch_id'] == s_id]
            s_idx = search.index

            # fill in missing values for orig_destination_distance
            num_nulls = search['orig_destination_distance'].isnull().values.sum()
            if num_nulls == len(search):
                # look for similar trips
                origin = search['visitor_location_country_id'].iloc[0]
                dest_id = search['srch_destination_id'].iloc[0]
                prop_country = search['prop_country_id'].iloc[0]

                same_trip = data_full.loc[
                    (data_full['visitor_location_country_id'] == origin) & ((data_full['srch_destination_id'] == dest_id) | (data_full['prop_country_id'])) == prop_country]

                avg_odd = same_trip['orig_destination_distance'].mean()

                # can still be nan, just use average distance to this booking...
                if isnan(avg_odd):
                    same_trip = data_full.loc[data_full['srch_destination_id'] == dest_id]
                    avg_odd = same_trip['orig_destination_distance'].mean()
                    std_odd = same_trip['orig_destination_distance'].std()
                    if isnan(avg_odd):
                        same_trip = data_full.loc[data_full['prop_country_id'] == prop_country]
                        avg_odd = same_trip['orig_destination_distance'].mean()
                        std_odd = same_trip['orig_destination_distance'].std()
                        if isnan(avg_odd):
                            print('Dest_id {} has no distance data at all!'.format(dest_id))
                else:
                    std_odd = same_trip['orig_destination_distance'].std()
            else:
                avg_odd = search['orig_destination_distance'].mean()
                std_odd = search['orig_destination_distance'].std()

            data.loc[s_idx, 'avg_orig_dest_dist'] = avg_odd
            data.loc[s_idx, 'std_orig_dest_dist'] = std_odd


        data.drop(columns=['orig_destination_distance'], inplace=True)

        data.to_csv('./data/train_split_cleaned3/train_data_{:02d}.csv'.format(i))

        print('Set {} saved'.format(i))

    print('--- DONE ---')
