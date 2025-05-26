from fias.app.db.db import (
        create_tables,
        upload_types,
        upload_hierarchy,
        upload_addresses
        )

if __name__ == '__main__':
    create_tables()
    upload_types()
    upload_hierarchy()
    upload_addresses()
    print('Done!')
