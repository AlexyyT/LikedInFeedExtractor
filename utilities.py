import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def open_driver(driver_path):
    driver = webdriver.Chrome(executable_path=driver_path)
    return driver


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_up(driver, scroll):
    driver.execute_script("window.scrollTo(0," + str(scroll) + ");")


def get_height(driver):
    return driver.execute_script("return document.body.scrollHeight")


def executor(driver, element):
    driver.execute_script("arguments[0].click();", element)


def get_soup(driver):
    page_source = driver.page_source
    soup = bs(page_source, "html")
    return soup


def linkedin_connexion(driver, email, mdp, pause):
    driver.get('https://www.linkedin.com/login')
    time.sleep(pause)
    driver.find_element(By.ID, "username").send_keys(email)
    time.sleep(pause)
    driver.find_element(By.ID, "password").send_keys(mdp)
    time.sleep(pause)
    driver.find_element(By.CLASS_NAME, 'btn__primary--large.from__button--floating').click()
    time.sleep(pause)


def get_wait(driver, second):
    return driver.WebDriverWait(driver, second)


def get_feed(driver, url, pause):
    driver.get(url)
    time.sleep(pause)

    SCROLL_PAUSE_TIME = pause

    # Get scroll height
    last_height = get_height(driver)

    # Scroll Down to finite the feed
    while True:
        scroll_down(driver)

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = get_height(driver)
        if new_height == last_height:
            break
        last_height = new_height

    # Scroll up to load all posts
    start_point = get_height(driver)
    while start_point > 0:
        scroll_level = -800
        start_point = start_point + scroll_level
        scroll_up(driver, start_point)
        time.sleep(SCROLL_PAUSE_TIME)

    soup = get_soup(driver)
    return soup


def get_comments(driver, soup, pause):
    pause = pause
    posts_class = 'ember-view occludable-update'
    body = driver.find_element(By.CLASS_NAME, 'render-mode-VANILLA.nav-v2.ember-application.icons-loaded.boot-complete')

    # Scraping du feed avec tous les posts
    posts = soup.find_all('div', {'class': posts_class})
    titre_class = 'update-components-text relative feed-shared-update-v2__commentary'

    for i in range(len(posts)):

        # Si le post a des commentaires =>
        if 'commentaire' not in posts[i].text:
            pass
        else:
            # R??cup??rer l'id du post
            post_id = posts[i]["id"]

            # Pause entre chaque post
            time.sleep(pause)
            # PATH du bouton pour afficher les commentaires
            try:
                PATH = "//div[@id='" + post_id + "']/div/div/div[6]/ul/li[2]/button"
                try:
                    # Trouve et clic deux fois sur le bouton pour afficher les commentaires
                    btn = driver.find_element(By.XPATH, PATH)
                    btn.click()
                    time.sleep(pause)
                    btn.click()
                except:
                    # Clique que la surcouche body.
                    wait = WebDriverWait(driver, 10)
                    executor(driver, body)
                    try:
                        # Clique sur premier post apr??s avoir enlev?? le layer du body.
                        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, PATH)))
                        showmore_link.click()
                        time.sleep(pause)
                        showmore_link.click()

                    except ElementClickInterceptedException:
                        print("Trying to click on the button again")
                        driver.execute_script("arguments[0].click()", showmore_link)
            # Si le path est en div[5] ?? la place de div[6] (car repost, donc moins de div)
            except:
                PATH = "//div[@id='" + post_id + "']/div/div/div[5]/ul/li[2]/button"
                try:
                    # Trouve et clic sur le bouton pour afficher les commentaires
                    btn = driver.find_element(By.XPATH, PATH)
                    btn.click()
                    time.sleep(pause)
                    btn.click()
                except:
                    # Clique que la surcouche body.
                    wait = WebDriverWait(driver, 10)
                    executor(driver, body)
                    try:
                        # Clique sur le premier post apr??s avoir enlev?? le layer ldu body.
                        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, PATH)))
                        showmore_link.click()
                        time.sleep(pause)
                        showmore_link.click()

                    except ElementClickInterceptedException:
                        print("Trying to click on the button again")
                        driver.execute_script("arguments[0].click()", showmore_link)

    soup = get_soup(driver)
    return soup


def get_reply(driver, soup, pause):
    pause = pause

    body = driver.find_element(By.CLASS_NAME, 'render-mode-VANILLA.nav-v2.ember-application.icons-loaded.boot-complete')
    verbatim_class = 'comments-comment-item comments-comments-list__comment-item'
    #Zc : Zone de commentaires - Elle comprend un commentaire ainsi que les potentielles r??ponses au commentaire.
    zc = soup.find_all('article', {'class': verbatim_class})

    for i in range(len(zc)):
        #Si la zone du commentaire n??cessite de charger des r??ponses pr??c??dentes.
        if 'Charger les r??ponses pr??c??dentes' not in zc[i].text:
            pass
        else:
            try:
                # Trouve et clic deux fois sur le bouton pour afficher les commentaires
                time.sleep(pause)
                PATH = "//article[@id='" + zc[i]['id'] + "']/div[4]/div[3]/div/button"
                btn = driver.find_element(By.XPATH, PATH)
                btn.click()
                time.sleep(pause)
            except:
                # Clique que la surcouche body.
                wait = WebDriverWait(driver, 10)
                executor(driver, body)
                try:
                    # Clique sur le premier post apr??s avoir enlev?? le layer ldu body.
                    showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, PATH)))
                    showmore_link.click()
                    time.sleep(pause)
                    showmore_link.click()
                except ElementClickInterceptedException:
                    print("Trying to click on the button again")
                    driver.execute_script("arguments[0].click()", showmore_link)


        # Si la zone du commentaire n??cessite d'afficher plus de r??ponses.
        if 'Afficher plus de r??ponses' not in zc[i].text:
            pass
        else:
            try:
                time.sleep(pause)
                PATH = "//article[@id='" + zc[i]['id'] + "']/div[4]/div[3]/div/button"
                btn = driver.find_element(By.XPATH, PATH)
                btn.click()
                time.sleep(pause)
            except:
                # Clique que la surcouche body.
                wait = WebDriverWait(driver, 10)
                executor(driver, body)
                try:
                    # Clique sur le premier post apr??s avoir enlev?? le layer ldu body.
                    showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, PATH)))
                    showmore_link.click()
                    time.sleep(pause)
                    showmore_link.click()
                except ElementClickInterceptedException:
                    print("Trying to click on the button again")
                    driver.execute_script("arguments[0].click()", showmore_link)

    soup = get_soup(driver)
    return soup


def get_scraping(soup):
    # Classes pour trouver tous les commentaires
    posts_class = 'ember-view occludable-update'
    verbatim_class = 'comments-comment-item comments-comments-list__comment-item'

    # Classes pour scraper chaque commentaire.
    titre_class = 'update-components-text relative feed-shared-update-v2__commentary'
    date_post_class = 'update-components-text-view white-space-pre-wrap break-words'
    author_class = 'comments-post-meta__name-text hoverable-link-text mr1'
    date_verbatim_class = 'comments-comment-item__timestamp t-12 t-black--light t-normal mr1'
    v_classe = 'comments-comment-item__main-content feed-shared-main-content--comment t-14 t-black t-normal'
    reponses = 'comments-comment-item comments-reply-item reply-item'

    # Df pour stocker les ??l??ments et exporter en .csv
    df = pd.DataFrame(columns=['Post', 'Post Date', 'Author', 'Verbatim', 'Verbatim Date', 'Date scraping'])

    # une fois que tous les commentaires sont ouverts, nouvelle soup pour scraper les ??l??ments
    posts = soup.find_all('div', {'class': posts_class})

    # Pour chaque post
    for i in range(len(posts)):
        # R??cup??rer l'id du post
        post_id = posts[i]["id"]

        # Si le post a des commentaires =>
        if 'commentaire' not in posts[i].text:
            pass
        else:

            #Auteur du post
            #  ???

            # Contenu du post
            title = soup.find('div', {'class': posts_class, 'id': post_id}) \
                .find_all('div', {'class': titre_class})
            contenu_post = title[0].text.replace('\n', '').replace('\xa0', ' ')

            # Date du post
            date = soup.find('div', {'class': posts_class, 'id': post_id}) \
                .find_all('div', {'class': date_post_class})
            date_post = date[0].text[:date[0].text.find(" ??? ")]

            # R??cup??re l'ensemble des commentaires sur le post
            verbatim = soup.find('div', {'class': posts_class, 'id': post_id})\
                .find_all('article', {'class': verbatim_class})

            # Pour chaque commentaire
            for i in range(len(verbatim)):
                article_id = verbatim[i]['id']

                # Auteur du verbatim
                author = soup.find('div', {'class': posts_class, 'id': post_id})\
                    .find('article', {'class': verbatim_class, 'id': article_id})\
                    .find_all('span', {'class': author_class})

                auteur = author[0].text[1:author[0].text.find('Voir')]

                # Verbatim
                verb = soup.find('div', {'class': posts_class, 'id': post_id})\
                    .find('article', {'class': verbatim_class, 'id': article_id})\
                    .find_all('span', {'class': v_classe})

                commentaire = verb[0].text.replace('\n', '')

                # Date du verbatim
                date_verbatim = soup.find('div', {'class': posts_class, 'id': post_id})\
                    .find('article', {'class': verbatim_class, 'id': article_id})\
                    .find_all('time', {'class': date_verbatim_class})

                # Ligne li??e au commentaire, ?? ajouter dans de df
                new_row = {'Post': contenu_post,
                           'Post Date': date_post,
                           'Author': auteur,
                           'Verbatim': commentaire,
                           'Verbatim Date': date_verbatim[0].text,
                           'Date scraping': datetime.now().strftime("%d/%m/%Y")
                           }

                # Ajout de la ligne contenant le commentaire dans le df
                df = df.append(new_row, ignore_index=True)


                # Zone de r??ponse  contient toutes les potentielles r??ponses ?? un commentaire.
                zr = soup.find('div', {'class': posts_class, 'id': post_id}).find('article', {'class': verbatim_class, 'id': article_id}).find_all('article', {'class': reponses})
                # Si la zone de r??ponse contient des r??ponses - Scrape et ajout les r??ponses au df.
                if len(zr) > 0:
                    # Pour chaque r??ponse : permet de g??rer s'il y a plusieurs r??ponses
                    for i in range(len(zr)):
                        #Num??ro du l'article li?? ?? la r??ponse ?? scrapper
                        reponse_id = zr[i]['id']

                        # Auteur
                        author = soup.find('div', {'class': posts_class, 'id': post_id})\
                            .find('article', {'class': verbatim_class, 'id': article_id})\
                            .find('article', {'class': reponses, 'id': reponse_id})\
                            .find('span', {'class': 'comments-post-meta__name-text hoverable-link-text mr1'})

                        auteur = author.text
                        auteur = auteur[1:(auteur.find('Voir'))]

                        # Verbatim
                        rep = soup.find('div', {'class': posts_class, 'id': post_id})\
                            .find('article', {'class': verbatim_class, 'id': article_id})\
                            .find('article', {'class': reponses, 'id': reponse_id})\
                            .find('span', {'class': 'comments-comment-item__main-content feed-shared-main-content--comment t-14 t-black t-normal'})

                        commentaire = rep.text
                        commentaire = commentaire.replace('\n', '')

                        # Date
                        time_rep = soup.find('div', {'class': posts_class, 'id': post_id})\
                            .find('article', {'class': verbatim_class, 'id': article_id})\
                            .find('article', {'class': reponses, 'id': reponse_id})\
                            .find('time', {'class': 'comments-comment-item__timestamp t-12 t-black--light t-normal mr1'})

                        date_verbatim = time_rep.text

                        # Ligne li??e ?? la r??ponse au commentaire ?? ajouter dans le df
                        new_row = {'Post': contenu_post,
                                   'Post Date': date_post,
                                   'Auteur': auteur,
                                   'Verbatim': commentaire,
                                   'Verbatim Date': date_verbatim,
                                   'Date scraping': datetime.now().strftime("%d/%m/%Y")
                                   }

                        # Ajout de la ligne contenant le commentaire dans le df
                        df = df.append(new_row, ignore_index=True)
    return df


def close_driver(driver):
    driver.close()


def export(df, filepath):
    df.to_csv(filepath, encoding='utf-16', sep=',', index=False)
