from fias.app.db import upload_data, create_tables


if __name__ == '__main__':
    create_tables()
    upload_data()
    print('Done!')
