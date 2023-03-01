from utilities import *
import sys

def main(url, filename):
    driver = open_driver("C:\\Users\\ATOU\\Downloads\\chromedriver_win32\\chromedriver.exe")

    pause = 2.5

    email = "toulou26@hotmail.fr"
    mdp = "AxyTmt26"

    linkedin_connexion(driver, email, mdp, pause)

    soup = get_feed(driver, url, pause)

    soup = get_comments(driver, soup, pause)

    soup = get_reply(driver, soup, pause)

    df = get_scraping(soup)

    close_driver(driver)

    filepath ='C:\\Users\\ATOU\\OneDrive - Axess OnLine\\Documents\\1. PROJETS\\PYTHON - LinkedIn Feed Extractor\\Files\\' + filename
    export(df, filepath)

if __name__ == '__main__':
    main('https://www.linkedin.com/company/la-boucherie-restaurants/posts/?feedView=all', 'lbchrie.csv')
   #main(sys.argv[2], sys.argv[3])

