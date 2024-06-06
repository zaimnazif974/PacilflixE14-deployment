GET_POPULAR_TAYANGAN = '''
WITH FILM_AND_SERIES_VIEWERS AS (
  SELECT F.id_tayangan, COUNT(start_date_time) AS total_view, \'film\' AS type
  FROM RIWAYAT_NONTON RN
  RIGHT OUTER JOIN FILM F ON 
    RN.id_tayangan = F.id_tayangan AND
    EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * F.durasi_film * 60
    AND  EXTRACT(DAY FROM NOW() - end_date_time) <= 7
  GROUP BY F.id_tayangan

  UNION

  SELECT S.id_tayangan, COUNT(start_date_time) AS total_view, \'series\' AS type
  FROM RIWAYAT_NONTON RN
  RIGHT OUTER JOIN (
    SELECT id_tayangan, SUM(E.durasi) as total_durasi_series
    FROM SERIES S
    JOIN EPISODE E ON E.id_series = S.id_tayangan
    GROUP BY id_tayangan
  ) S ON 
    RN.id_tayangan = S.id_tayangan AND
    EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * S.total_durasi_series * 60
    AND  EXTRACT(DAY FROM NOW() - end_date_time) <= 7
  GROUP BY S.id_tayangan
)

SELECT *
FROM FILM_AND_SERIES_VIEWERS AS VIEWERS
JOIN TAYANGAN T ON VIEWERS.id_tayangan =  T.id
ORDER BY VIEWERS.total_view DESC, release_date_trailer DESC
LIMIT 10;
'''

GET_SEARCH_TAYANGAN = '''
  SELECT tayangan.*, \'film\' AS type
  FROM tayangan 
  JOIN film ON tayangan.id = film.id_tayangan
  WHERE judul ILIKE %(keyword)s

  UNION

  SELECT tayangan.*, \'series\' AS type
  FROM tayangan
  JOIN series ON tayangan.id = series.id_tayangan
  WHERE judul ILIKE %(keyword)s;
'''

GET_FILM_DETAIL = '''
    SELECT id, judul, sinopsis, asal_negara, id_sutradara, url_video_film, release_date_film, durasi_film, total_view, avg_rating
    FROM (
        SELECT *
        FROM TAYANGAN
        WHERE id=%s
    ) AS T
    JOIN FILM  F ON F.id_tayangan=T.id
    JOIN FILM_VIEWERS FV ON FV.id_tayangan=T.id
    JOIN AVERAGE_RATING AR ON AR.id_tayangan=T.id;
'''

GET_SERIES_DETAIL = '''
    SELECT id, judul, sinopsis, asal_negara, id_sutradara, total_view, avg_rating
    FROM (
        SELECT *
        FROM TAYANGAN
        WHERE id=%s
    ) AS T
    JOIN SERIES S ON S.id_tayangan=T.id
    JOIN SERIES_VIEWERS SV ON SV.id_tayangan=T.id
    JOIN AVERAGE_RATING AR ON AR.id_tayangan=T.id;
'''

GET_EPISODE_BY_SERIES_ID = '''
    SELECT sub_judul, sinopsis, durasi, url_video, release_date
    FROM EPISODE
    WHERE id_series=%s;
'''

GET_SUTRADARA_BY_ID = '''
    SELECT id, nama, jenis_kelamin, kewarganegaraan
    FROM CONTRIBUTORS
    WHERE id=%s;
'''

GET_GENRE_BY_TAYANGAN_ID = '''SELECT genre FROM GENRE_TAYANGAN WHERE id_tayangan=%s;'''

GET_PEMAIN_BY_TAYANGAN_ID = '''
    SELECT id, nama, jenis_kelamin, kewarganegaraan
    FROM MEMAINKAN_TAYANGAN MT
    JOIN CONTRIBUTORS C ON MT.id_pemain=C.id
    WHERE MT.id_tayangan=%s;
'''

GET_PENULIS_SKENARIO_BY_TAYANGAN_ID = '''
    SELECT id, nama, jenis_kelamin, kewarganegaraan
    FROM MENULIS_SKENARIO_TAYANGAN MST
    JOIN CONTRIBUTORS C ON MST.id_penulis_skenario=C.id
    WHERE MST.id_tayangan=%s;
'''

GET_EPISODE_BY_ID = '''
    SELECT id_series, judul, sub_judul, E.sinopsis, E.durasi, url_video, release_date
    FROM (
      SELECT * 
      FROM EPISODE
      WHERE id_series=%s AND sub_judul=%s
    ) AS E
    JOIN TAYANGAN T ON T.id=E.id_series;
'''

GET_OTHER_EPISODES = '''
    SELECT * 
    FROM EPISODE
    WHERE id_series=%s AND sub_judul<>%s;
'''

GET_DURASI_TAYANGAN = '''
  SELECT id_series, SUM(durasi) as durasi
  FROM episode
  WHERE id_series=%(id)s
  GROUP BY id_series

  UNION

  SELECT id_tayangan, durasi_film as durasi
  FROM film
  WHERE id_tayangan=%(id)s;
'''

CREATE_VIEW_FILM_VIEWERS = '''
  CREATE OR REPLACE VIEW FILM_VIEWERS AS
  SELECT F.id_tayangan, COUNT(start_date_time) AS total_view
  FROM RIWAYAT_NONTON RN
  RIGHT OUTER JOIN FILM F ON 
    RN.id_tayangan = F.id_tayangan AND
    EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * F.durasi_film * 60
  GROUP BY F.id_tayangan;
'''

CREATE_VIEW_SERIES_VIEWERS = '''
  CREATE OR REPLACE VIEW SERIES_VIEWERS AS
  SELECT S.id_tayangan, COUNT(start_date_time) AS total_view
  FROM RIWAYAT_NONTON RN
  RIGHT OUTER JOIN (
    SELECT id_tayangan, SUM(E.durasi) as total_durasi_series
    FROM SERIES S
    JOIN EPISODE E ON E.id_series = S.id_tayangan
    GROUP BY id_tayangan
  ) S ON 
    RN.id_tayangan = S.id_tayangan AND
    EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * S.total_durasi_series * 60
  GROUP BY S.id_tayangan;
'''

CREATE_VIEW_AVERAGE_RATING = '''
  CREATE OR REPLACE VIEW AVERAGE_RATING AS
  SELECT id_tayangan, ROUND(AVG(rating),1) as avg_rating
  FROM ULASAN U
  GROUP BY id_tayangan;
'''