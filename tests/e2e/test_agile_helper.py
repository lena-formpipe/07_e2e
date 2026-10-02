import re #reguljära uttryck == regex
from playwright.sync_api import Page, expect
import pytest


# User story:
# Som en användare
# vill jag kunna läsa sidans title
# så att jag vet att jag är på rätt sida
# 1. Navigera till sidan Agile helper
# 2. Kontrollera att sidans title är "Agile helper"

def test_has_title(page:Page, url):
    # arrange = fixture page, act = goto
    page.goto(url)

    # expect at title "to contain" a substring, re.compile tillåter tex ! i slutet
    expect(page).to_have_title(re.compile("Agile helper"))

####################################################################################
# user story:
# som en användare
# vill jag kunna läsa om Sprint retrospective
# så att jag slutar en sprint på rätt sätt
# 1.	Navigera till sidan Agile helper
# 2.	Klicka på knappen med texten ”sista” (implicit test av knapp)
# 3.	Klicka på knappen med texten ”sprint retrospective” (implicit test av knapp)
# 4.	Leta upp rubriken <h2> sprint retrospective på sidan
# 5.	Kontrollera att rubriken är synlig (kan vara del av steg 4)

@pytest.mark.smoke
def test_read_sprint_retrospective(page:Page, url):
    # surfa till sidan
    page.goto(url) #

    # klicka på knappen sista
    button_locator = page.get_by_role("button")
    button_last = button_locator.get_by_text("Sista")
    button_last.click()

    # klicka på knappen retrospective
    page.get_by_role("button").get_by_text(re.compile("Sprint retrospective")).click()

    #Leta upp heading h2
    heading = page.get_by_role("heading").get_by_text(re.compile("Sprint retrospective"))

    # kontrollera att heading är synlig
    expect(heading).to_be_visible()


####################################################################################
# user story:
# Story: Som en användare,
# vill jag se mötet "sprint planning" som utspelar sig första dagen på en sprint,
# så att jag vet vad jag ska göra på mötet.

# Scenario:
# 1.	Navigera till webbsidan https://lejonmanen.github.io/agile-helper/
# 2.	Klicka på knappen med texten "första"
# 3.	Klicka på knappen vars text innehåller "Sprint planning"
# 4.	Kontrollera att ett <h2> element visas på sidan, som innehåller en rubrik med texten "Sprint planning"

def test_read_sprint_planning(page:Page, url):
    # surfa till sidan
    page.goto(url)

    # klicka på knappen första
    button_locator = page.get_by_role("button")
    button_first = button_locator.get_by_text("Första")
    button_first.click()

    # klicka på knappen "sprint planning"
    page.get_by_role("button").get_by_text(re.compile("Sprint planning")).click()

    #Leta upp heading h2
    heading = page.get_by_role("heading").get_by_text(re.compile("Sprint planning"))

    # kontrollera att heading är synlig
    expect(heading).to_be_visible()

####################################################################################
    # user story:
    # Story: Som en användare,
    # vill jag utföra "daily standup" varje dag under sprintens gång,
    # så att jag vet vad jag ska göra på mötet.

    # Scenario:
    # 1. Navigera till webbsidan https://lejonmanen.github.io/agile-helper/
    # 2. Klicka på knappen med texten "någonstans mitt i"
    # 3. Klicka på knappen vars text innehåller "Daily standup"
    # 4. Klicka på knappen börja mötet
    # 5. Kontrollera att knappen "börja mötet" är inaktiverad
    # 6. Kontrollera att ett <h2> element visas på sidan, som innehåller en rubrik med texten "Sprint planning"
    # 7. Klicka på knappen "mötet slut"
    # 8. Kontrollera att rubriken "Sprint planning" inte längre visas.

def test_do_daily_standup(page: Page, url):
    # surfa till sidan
    page.goto(url)

    # klicka på knappen första
    button_locator = page.get_by_role("button")
    button_middle = button_locator.get_by_text("mitt i")
    button_middle.click()

    # klicka på knappen "sprint planning"
    page.get_by_role("button").get_by_text(re.compile("Daily standup")).click()

    # Leta upp heading h2
    heading = page.get_by_role("heading").get_by_text(re.compile("Daily standup"))

    # kontrollera att heading är synlig
    expect(heading).to_be_visible()

    # klicka på knappen "börja mötet"
    button_locator = page.get_by_role("button")
    button_start_meeting = button_locator.get_by_text(re.compile("Börja mötet"))
    button_start_meeting.click()
   # page.get_by_role("button").get_by_text(re.compile("Börja mötet")).click()

    # kontrollera att knappen börja mötet har inaktiverats
    expect(button_start_meeting).to_be_disabled()

    # Klicka för att avsluta mötet.
    page.get_by_role("button").get_by_text(re.compile("mötet slut")).click()

    # kontrollera att daily standup avslutats och inte visas längre
    # För att göra detta måste jag använda class sprint-ceremony.dialog
    dialog = page.locator(".sprint-ceremony.dialog").filter(has=page.get_by_role("heading", name=re.compile("Daily standup") ))
    # vänta en stund så att transitionen inträffat och opacity är 0 samt dialog hight = 0px
    page.wait_for_timeout(600)

    # Debug
    print("dialog count:", dialog.count())
    print("dialog opacity:", dialog.evaluate("(e) => getComputedStyle(e).opacity"))
    print("dialog hight:", dialog.evaluate("(e) => getComputedStyle(e).height"))

    # assert
    expect(dialog).to_have_css("opacity", "0")
    expect(dialog).to_have_css("max-height", "0px")




