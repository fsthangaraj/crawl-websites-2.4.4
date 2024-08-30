import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv

# Process the anchor tag according to the given JavaScript logic
def process_anchor_tag(element):
    try:
        hasTitle = element.has_attr('title')
        hasHref = element.has_attr('href')
        hasAriaHidden = element.has_attr('aria-hidden')
        anchorText = (element.text or '').strip()
        ariaLabel = element.get('aria-label', '').strip()

        if ariaLabel:
            return None
        if any(img.get('alt', '').strip() for img in element.find_all('img')):
            return None

        if hasTitle:
            titleVal = element.get('title', '').strip()
            if not hasHref:
                if anchorText == "":
                    if hasAriaHidden:
                        return None
                    else:
                        return "2_4_4_H77,H78,H79,H80,H81,H33", "HTMLCS.WARNING"
                elif anchorText != titleVal:
                    return None
                else:
                    return "2_4_4_H77,H78,H79,H80,H81,H33", "HTMLCS.WARNING"
            else:
                hrefVal = element.get('href', '').strip()
                if titleVal and not hrefVal:
                    return "2_4_4_H77,H78,H79,H80,H81,H33", "HTMLCS.WARNING"
                elif not titleVal:
                    if hrefVal and anchorText:
                        return "2_4_4_H77,H78,H79,H80,H81", "HTMLCS.NOTICE"
                    else:
                        return "2_4_4_H77,H78,H79,H80,H81", "HTMLCS.WARNING"
                elif not anchorText:
                    return "2_4_4_H77,H78,H79,H80,H81,H33", "HTMLCS.NOTICE"
                elif anchorText == titleVal:
                    return "2_4_4_H77,H78,H79,H80,H81,H33", "HTMLCS.WARNING"
                else:
                    return "2_4_4_H77,H78,H79,H80,H81,H33", "HTMLCS.NOTICE"
        else:
            if not hasHref:
                if anchorText == "":
                    if hasAriaHidden:
                        return None
                    else:
                        return "2_4_4_H77,H78,H79,H80,H81", "HTMLCS.WARNING"
                else:
                    return "2_4_4_H77,H78,H79,H80,H81", "HTMLCS.WARNING"
            else:
                if hasHref and anchorText:
                    return "2_4_4_H77,H78,H79,H80,H81", "HTMLCS.NOTICE"
                elif anchorText or hasAriaHidden:
                    return None
                else:
                    return "2_4_4_H77,H78,H79,H80,H81", "HTMLCS.WARNING"
    except Exception as e:
        print(f"Error processing anchor tag: {e}")
        return None

async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Failed to retrieve {url}: Status code {response.status}")
                return None
    except asyncio.TimeoutError:
        print(f"Timeout occurred while fetching {url}")
    except Exception as e:
        print(f"Exception occurred while fetching {url}: {e}")
    return None

async def crawl_and_process(session, url):
    html = await fetch_html(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    anchor_tags = soup.find_all('a')
    results = []

    for index, tag in enumerate(anchor_tags, start=1):
        result = process_anchor_tag(tag)
        if result:
            rule, severity = result
            tag_str = str(tag)
            results.append((index, url, tag_str, rule, severity))
    
    return results

async def crawl_websites(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [crawl_and_process(session, url) for url in urls]
        all_results = []
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                all_results.extend(result)
            except Exception as e:
                print(f"An error occurred while processing a task: {e}")
        return all_results

def main(urls, output_csv='output.csv'):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(crawl_websites(urls))
    
    if results:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['s.no', 'url', 'tag', 'rule', 'severe']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                s_no, url, tag, rule, severe = result
                writer.writerow({'s.no': s_no, 'url': url, 'tag': tag, 'rule': rule, 'severe': severe})

        print(f"Results saved to CSV file: {output_csv}")
    else:
        print("No results to save.")

if __name__ == "__main__":
    websites = [
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.nytimes.com",
    "https://www.theguardian.com",
    "https://www.foxnews.com",
    "https://www.aljazeera.com",
    "https://www.reuters.com",
    "https://www.huffpost.com",
    "https://www.npr.org",
    "https://www.bloomberg.com",
    "https://www.forbes.com",
    "https://www.wsj.com",
    "https://www.usatoday.com",
    "https://www.cbsnews.com",
    "https://www.abcnews.go.com",
    "https://www.nbcbayarea.com",
    "https://www.latimes.com",
    "https://www.chicagotribune.com",
    "https://www.nbcnews.com",
    "https://www.buzzfeednews.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.tiktok.com",
    "https://www.snapchat.com",
    "https://www.pinterest.com",
    "https://www.reddit.com",
    "https://www.quora.com",
    "https://www.tumblr.com",
    "https://www.medium.com",
    "https://www.discord.com",
    "https://www.slack.com",
    "https://www.telegram.org",
    "https://www.whatsapp.com",
    "https://www.wechat.com",
    "https://www.weibo.com",
    "https://www.vk.com",
    "https://www.line.me",
    "https://www.sina.com.cn",
    "https://www.amazon.com",
    "https://www.ebay.com",
    "https://www.walmart.com",
    "https://www.alibaba.com",
    "https://www.etsy.com",
    "https://www.shopify.com",
    "https://www.bestbuy.com",
    "https://www.target.com",
    "https://www.zappos.com",
    "https://www.newegg.com",
    "https://www.homedepot.com",
    "https://www.lowes.com",
    "https://www.costco.com",
    "https://www.samsclub.com",
    "https://www.wayfair.com",
    "https://www.overstock.com",
    "https://www.macys.com",
    "https://www.nordstrom.com",
    "https://www.sephora.com",
    "https://www.ulta.com",
    "https://www.google.com",
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.techcrunch.com",
    "https://www.wired.com",
    "https://www.cnet.com",
    "https://www.mashable.com",
    "https://www.arstechnica.com",
    "https://www.engadget.com",
    "https://www.theverge.com",
    "https://www.ted.com",
    "https://www.kickstarter.com",
    "https://www.producthunt.com",
    "https://www.codepen.io",
    "https://www.dribbble.com",
    "https://www.behance.net",
    "https://www.medium.com",
    "https://www.twitch.tv",
    "https://www.coursera.org",
    "https://www.edx.org",
    "https://www.khanacademy.org",
    "https://www.udemy.com",
    "https://www.udacity.com",
    "https://www.pluralsight.com",
    "https://www.lynda.com",
    "https://www.skillshare.com",
    "https://www.futurelearn.com",
    "https://www.classcentral.com",
    "https://www.codecademy.com",
    "https://www.dataquest.io",
    "https://www.brilliant.org",
    "https://www.edureka.co",
    "https://www.alison.com",
    "https://www.openlearning.com",
    "https://www.simplilearn.com",
    "https://www.linkedin.com/learning",
    "https://www.treehouse.com",
    "https://www.academicearth.org",
    "https://www.booking.com",
    "https://www.airbnb.com",
    "https://www.expedia.com",
    "https://www.tripadvisor.com",
    "https://www.priceline.com",
    "https://www.hotels.com",
    "https://www.kayak.com",
    "https://www.skyscanner.com",
    "https://www.trivago.com",
    "https://www.travelocity.com",
    "https://www.agoda.com",
    "https://www.orbitz.com",
    "https://www.cheapoair.com",
    "https://www.ihg.com",
    "https://www.marriott.com",
    "https://www.hilton.com",
    "https://www.hyatt.com",
    "https://www.raddisonhotels.com",
    "https://www.accorhotels.com",
    "https://www.wyndhamhotels.com",
    "https://www.netflix.com",
    "https://www.hulu.com",
    "https://www.disneyplus.com",
    "https://www.amazon.com/primevideo",
    "https://www.youtube.com",
    "https://www.spotify.com",
    "https://www.apple.com/apple-tv-plus",
    "https://www.hbo.com",
    "https://www.showtime.com",
    "https://www.paramountplus.com",
    "https://www.peacocktv.com",
    "https://www.sling.com",
    "https://www.fubo.tv",
    "https://www.tubi.tv",
    "https://www.crunchyroll.com",
    "https://www.funimation.com",
    "https://www.vudu.com",
    "https://www.roku.com",
    "https://www.sonycrackle.com",
    "https://www.pluto.tv",
    "https://www.webmd.com",
    "https://www.mayoclinic.org",
    "https://www.healthline.com",
    "https://www.medlineplus.gov",
    "https://www.nih.gov",
    "https://www.cdc.gov",
    "https://www.who.int",
    "https://www.drugs.com",
    "https://www.medscape.com",
    "https://www.everydayhealth.com",
    "https://www.healthychildren.org",
    "https://www.menshealth.com",
    "https://www.womenshealthmag.com",
    "https://www.fitnessmagazine.com",
    "https://www.livestrong.com",
    "https://www.shape.com",
    "https://www.prevention.com",
    "https://www.runnersworld.com",
    "https://www.self.com",
    "https://www.nutrition.gov",
    "https://www.paypal.com",
    "https://www.chase.com",
    "https://www.wellsfargo.com",
    "https://www.bankofamerica.com",
    "https://www.citi.com",
    "https://www.capitalone.com",
    "https://www.discover.com",
    "https://www.americanexpress.com",
    "https://www.fidelity.com",
    "https://www.vanguard.com",
    "https://www.robinhood.com",
    "https://www.wealthfront.com",
    "https://www.betterment.com",
    "https://www.nerdwallet.com",
    "https://www.investopedia.com",
    "https://www.morningstar.com",
    "https://www.bloomberg.com",
    "https://www.marketwatch.com",
    "https://www.barrons.com",
    "https://www.forbes.com",
    "https://www.allrecipes.com",
    "https://www.foodnetwork.com",
    "https://www.epicurious.com",
    "https://www.bonappetit.com",
    "https://www.yummly.com",
    "https://www.seriouseats.com",
    "https://www.simplyrecipes.com",
    "https://www.delish.com",
    "https://www.tasty.co",
    "https://www.chowhound.com",
    "https://www.eater.com",
    "https://www.food.com",
    "https://www.marthastewart.com",
    "https://www.thekitchn.com",
    "https://www.skinnytaste.com",
    "https://www.smittenkitchen.com",
    "https://www.loveandlemons.com",
    "https://www.cookieandkate.com",
    "https://www.101cookbooks.com",
    "https://www.foodandwine.com",
    "https://www.espn.com",
    "https://www.nfl.com",
    "https://www.nba.com",
    "https://www.mlb.com",
    "https://www.nhl.com",
    "https://www.cbssports.com",
    "https://www.foxsports.com",
    "https://www.bleacherreport.com",
    "https://www.si.com",
    "https://www.sportingnews.com",
    "https://www.sbnation.com",
    "https://www.goal.com",
    "https://www.soccer.com",
    "https://www.uefa.com",
    "https://www.fifa.com",
    "https://www.ussoccer.com",
    "https://www.premierleague.com",
    "https://www.espncricinfo.com",
    "https://www.rugbyworldcup.com",
    "https://www.olympic.org",
    "https://www.vogue.com",
    "https://www.gq.com",
    "https://www.harpersbazaar.com",
    "https://www.elle.com",
    "https://www.cosmopolitan.com",
    "https://www.instyle.com",
    "https://www.marieclaire.com",
    "https://www.refinery29.com",
    "https://www.glossy.co",
    "https://www.allure.com",
    "https://www.vanityfair.com",
    "https://www.wmagazine.com",
    "https://www.popsugar.com",
    "https://www.thecut.com",
    "https://www.whowhatwear.com",
    "https://www.byrdie.com",
    "https://www.wellandgood.com",
    "https://www.manrepeller.com",
    "https://www.theringer.com",
    "https://www.highsnobiety.com",
    "https://www.autotrader.com",
    "https://www.cars.com",
    "https://www.kbb.com",
    "https://www.edmunds.com",
    "https://www.motortrend.com",
    "https://www.caranddriver.com",
    "https://www.roadandtrack.com",
    "https://www.autoblog.com",
    "https://www.jdpower.com",
    "https://www.truecar.com",
    "https://www.cargurus.com",
    "https://www.carfax.com",
    "https://www.tesla.com",
    "https://www.ford.com",
    "https://www.toyota.com",
    "https://www.chevrolet.com",
    "https://www.honda.com",
    "https://www.nissanusa.com",
    "https://www.bmwusa.com",
    "https://www.mercedes-benz.com"
]

    main(websites)
