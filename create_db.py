from __future__ import print_function
import pandas as pd
import sys
from mongoengine import *
from models import Area

connect('provinces')


def load_data_to_db(row):
    province_id = int(row['CH_ID'])
    province = Area.objects(aid=province_id).first()
    if not province:
        try:
            province = Area(
                level='ch',
                th_name=row['CHANGWAT_T'].split()[-1],
                en_name=row['CHANGWAT_E'],
                aid=province_id
            )
            province.save()
        except ValidationError as e:
            print(row['CHANGWAT_T'], row['CHANGWAT_E'])

    amphoe_id = int(row['AM_ID'])
    amphoe = Area.objects(aid=amphoe_id).first()
    if not amphoe:
        try:
            amphoe = Area(
                level='am',
                th_name=row['AMPHOE_T'].split()[1],
                en_name=row['AMPHOE_E'],
                aid=amphoe_id,
                parent=province
            )
            amphoe.save()
        except ValidationError as e:
            print(row['AMPHOE_E'], row['AMPHOE_T'])

    tambon_id = int(row['TA_ID'])
    tambon = Area.objects(aid=tambon_id).first()
    if not tambon:
        try:
            tambon = Area(
                level='ta',
                th_name=row['TAMBON_T'].split()[1],
                aid=tambon_id,
                parent=amphoe,
                latlng=[float(row['LONG']), float(row['LAT'])],
            )
            tambon.save()
        except ValidationError as e:
            print(row['TAMBON_E'], row['TAMBON_T'])
            sys.exit(1)
    else:
        # the tambon exists, do nothing.
        '''
        print('{}, {}, {} already in the database'.format(
            tambon.th_name.encode('utf8'),
            amphoe.th_name.encode('utf8'),
            province.th_name.encode('utf8')
        ))
        '''
        return

    amphoe.childs.append(tambon)
    amphoe.save()

    province.childs.append(amphoe)
    province.save()


def main(data_file):
    data = pd.read_excel(data_file)
    data.apply(load_data_to_db, axis=1)


if __name__=='__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python createdb.py <excel file>", file=sys.stderr)
