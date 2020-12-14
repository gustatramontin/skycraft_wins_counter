import imgkit

def create_rank_image(rank, page):

    rank_table = "<div class='rank'><table><tr><th>#</th><th>Jogador</th><th>Vitórias</th></tr>"

    new_rank = rank[(page-1)*20:page*(20)] 
    if page == 1:
        i = 1
    else:
        i = ((page-1) * 20)+1

    for row in new_rank:
        name = row[0]
        wins = row[3]
        img_path = row[2]
        
        if i == 1:
            rank_table += f"<tr class='first'><td>{i}</td><td class='name'><img src='{img_path}'>{name}</td><td>{wins}</td></tr>"
        elif i == 2:
            rank_table += f"<tr class='second'><td>{i}</td><td class='name'><img src='{img_path}'>{name}</td><td>{wins}</td></tr>"
        elif i == 3:
            rank_table += f"<tr class='third'><td>{i}</td><td class='name'><img src='{img_path}'>{name}</td><td>{wins}</td></tr>"
        else:
            rank_table += f"<tr class='normal'><td>{i}</td><td class='name'><img src='{img_path}'>{name}</td><td>{wins}</td></tr>"

        i += 1

    rank_table += "</table></div>"
    css = """
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

        * {
            font-family: 'Open Sans', sans-serif;

        }

        .rank {
            width: 1000px;
        }

        table {
            width: 100%;
            border-spacing: 3.5px;
        }
    
        img {
            width: 40px;
            height: 40px;
        }

        th {
            border: 1px solid #d2d2d2;
        }

        .first {
            background-color: rgba(245, 228, 4, .41) !important;
        }

        .second {
            background-color: #f1efef !important;
        }

        .third {
            background-color: rgba(216, 65, 29, .29) !important;
        }

        tr:nth-child(even) {
            background-color: #f1efef;
        }

        td,
        th {
            padding: 10px auto;
            font-size: 2.7rem;
            font-weight: normal;
        }

        td {
            text-align: center;
            padding: 10px;
        }

        .name {
            text-align: left;
        }
    """
    html = f"""
        <html>
            <head>
            <meta charset='UTF-8'>
            <style>
            {css}
            </style>
            </head>
            <body>
            {rank_table}
            </body>
        </html>    
    """

    
    config = imgkit.config(wkhtmltoimage='/usr/local/bin/wkhtmltoimage')
    imgkit.from_string(html, 'rank.jpg', config=config)

if __name__ == "__main__":
    pass