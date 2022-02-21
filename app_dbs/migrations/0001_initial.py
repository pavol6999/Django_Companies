# Generated by Django 3.1 on 2021-03-24 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("""CREATE TABLE ov.companies(
                                cin bigint NOT NULL,
                                name character varying,
                                br_section character varying,
                                address_line character varying,
                                last_update timestamp without time zone,
                                created_at timestamp without time zone,
                                updated_at timestamp without time zone,
                                CONSTRAINT companies_pkey PRIMARY KEY (cin)
                            );
                            """),

        migrations.RunSQL("""INSERT INTO ov.companies(cin, name, br_section, address_line, last_update, created_at, updated_at)
                            SELECT  cin, corporate_body_name, br_section, CASE WHEN street is not NULL and city is not null and postal_code is not null THEN concat(street,', ',postal_code,' ',city)
                                          ELSE address_line END AS address_line, updated_at as last_update, now(), now()
                            FROM (SELECT *,RANK() OVER(PARTITION BY cin ORDER BY updated_at DESC)  FROM ov.or_podanie_issues) ano WHERE rank = 1 and cin is not NULL
                            ON CONFLICT DO NOTHING;"""),
                            
        migrations.RunSQL("""INSERT INTO ov.companies(cin, name, br_section, address_line, last_update, created_at, updated_at)
                            SELECT cin, corporate_body_name, br_section, 
                                            CASE WHEN street is not NULL and city is not null and postal_code is not null THEN concat(street,', ',postal_code,' ',city)
                                            ELSE NULL END AS address_line, updated_at as last_update, now(), now()
                            FROM (SELECT *, RANK() OVER(PARTITION BY cin ORDER BY updated_at DESC) FROM ov.likvidator_issues) hm WHERE rank = 1 and cin is not NULL
                            ON CONFLICT DO NOTHING;
                            """),

        migrations.RunSQL("""INSERT INTO ov.companies(cin, name, br_section, address_line, last_update, created_at, updated_at)
                            SELECT cin, corporate_body_name, NULL as br_section, 
                                            CASE WHEN street is not NULL and city is not null and postal_code is not null THEN concat(street,', ',postal_code,' ',city)
                                            ELSE NULL END AS address_line, updated_at as last_update, now(), now()
                            FROM (SELECT *, RANK() OVER(PARTITION BY cin ORDER BY updated_at DESC) FROM ov.konkurz_vyrovnanie_issues) hm WHERE rank = 1 and cin is not NULL
                            ON CONFLICT DO NOTHING;"""),

        migrations.RunSQL("""INSERT INTO ov.companies(cin, name, br_section, address_line, last_update, created_at, updated_at)
                            SELECT cin, corporate_body_name, br_section, 
                                            CASE WHEN street is not NULL and city is not null and postal_code is not null THEN concat(street,', ',postal_code,' ',city)
                                            ELSE NULL END AS address_line, updated_at as last_update, now(), now()
                            FROM (SELECT *, RANK() OVER(PARTITION BY cin ORDER BY updated_at DESC) FROM ov.znizenie_imania_issues) hm WHERE rank = 1 and cin is not NULL
                            ON CONFLICT DO NOTHING;"""),
        

        migrations.RunSQL("""INSERT INTO ov.companies(cin, name, br_section, address_line, last_update, created_at, updated_at)
                                SELECT cin, corporate_body_name, NULL as br_section, 
                                            CASE WHEN street is not NULL and city is not null and postal_code is not null THEN concat(street,', ',postal_code,' ',city)
                                            ELSE NULL END AS address_line, updated_at as last_update, now(), now()
                            FROM (SELECT *, RANK() OVER(PARTITION BY cin ORDER BY updated_at DESC) FROM ov.konkurz_restrukturalizacia_actors) hm WHERE rank = 1 and cin is not null
                            ON CONFLICT DO NOTHING;"""),
        migrations.RunSQL("""ALTER TABLE ov.likvidator_issues
                            ADD COLUMN company_id bigint,
                            ADD FOREIGN KEY (company_id) REFERENCES ov.companies(cin);

                            UPDATE ov.likvidator_issues
                            set company_id=cin;
                            """),
        migrations.RunSQL("""ALTER TABLE ov.konkurz_vyrovnanie_issues
                            ADD COLUMN company_id bigint,
                            ADD FOREIGN KEY (company_id) REFERENCES ov.companies(cin);

                            UPDATE ov.konkurz_vyrovnanie_issues
                            set company_id=cin;
                            """),
        migrations.RunSQL("""ALTER TABLE ov.konkurz_restrukturalizacia_actors
                            ADD COLUMN company_id bigint,
                            ADD FOREIGN KEY (company_id) REFERENCES ov.companies(cin);

                            UPDATE ov.konkurz_restrukturalizacia_actors
                            set company_id=cin;
                            """),
        migrations.RunSQL("""ALTER TABLE ov.znizenie_imania_issues
                            ADD COLUMN company_id bigint,
                            ADD FOREIGN KEY (company_id) REFERENCES ov.companies(cin);

                            UPDATE ov.znizenie_imania_issues
                            set company_id=cin;
                            """),
        migrations.RunSQL("""ALTER TABLE ov.or_podanie_issues
                            ADD COLUMN company_id bigint,
                            
                            ADD FOREIGN KEY (company_id) REFERENCES ov.companies(cin);
                            

                            UPDATE ov.or_podanie_issues
                            set company_id=cin
                            
                            """)

    ]