import pygame
import time as clock
import textwrap
import numpy as np
import copy
import time
import random

from scipy.ndimage import gaussian_filter
from player import Player
from player_in_combat import PlayerInCombat
from npc import Npc
from scene import Scene
from npc_in_combat import NpcInCombat

class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, action = None):
        super().__init__()
        self.original_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hover = False
        self.width = width
        self.action = action
        self.start_game = False

    def button_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        self.hover = self.rect.collidepoint(mouse_pos)
        global xlCookingPot, turn

        if self.hover and mouse_buttons[0]:  # Left mouse button is pressed
            if self.action == "play":
                self.start_game = True
            elif self.action == "exit":
                pygame.quit()
                quit()
            elif self.action == "pick_ingredient":
                time.sleep(0.5)
                if len(xlCookingPot) < 4:
                    global inventory_toggle
                    inventory_toggle = True
                    return
                else:
                    global message
                    message = "You can only pick 4 ingredients. Time to cook!"
                    return
            elif self.action == "cook":
                time.sleep(0.5)
                if len(xlCookingPot) == 4:
                    if check_recipe(xlCookingPot, valid_recipes):

                        combatXl.take_damage(100)
                        xlCookingPot.clear()
                        return
                    else:
                        turn = 'enemy'
                        xlCookingPot.clear()
                        message = "You cooked the wrong dish!"
                        return
                else:
                    message = "You need 4 ingredients to cook!"
                    return
            elif self.action == "advice":
                time.sleep(0.5)
                file = open("Dialogues/xl_advice", "r")
                message = random.choice(file.readlines())
                file.close()
                return
            elif self.action == "feed":
                time.sleep(0.5)
                if current_scene.goubaIndex < 6:

                    goubaFile = open("Dialogues/gouba", "r")
                    message = goubaFile.readlines();
                    message = message[current_scene.goubaIndex]
                    goubaFile.close()

                    current_scene.goubaIndex += 1
                    if current_scene.goubaIndex == 6:
                        global goubaAchievement, achievementList
                        obtainAchievement(achievementList, "Gouba? Gouba!")
                        goubaAchievement = True
                return
            elif self.action == "attack":
                time.sleep(0.5)
                current_scene.get_npc().take_damage(10)
                message = "You attacked the slime!"

                turn = 'enemy'
                return
            elif self.action == "special":
                time.sleep(0.5)
                current_scene.get_npc().take_damage(20)
                message = "Yelan used her special attack! 'Lifeline'!"

                turn = 'enemy'
                return
            elif self.action == "flee":
                time.sleep(0.5)
                current_scene.get_player().take_damage(100)
                message = "You ran away!"
                return
            elif self.action == "talk":
                time.sleep(0.5)
                file = open("Dialogues/slime", "r")
                message = random.choice(file.readlines())
                turn = 'enemy'
                if message.__contains__("10 damage"):
                    current_scene.get_player().take_damage(10)
                    turn = 'player'
                return
            elif self.action == "analyze":
                time.sleep(0.5)
                if len(current_inventory) == 0:
                    message = "You have no ideas to analyze! Try reading some minds first!"
                    return
                elif len(xlCookingPot) < 3:
                    inventory_toggle = True
                    return
                else:
                    message = "You can only pick 3 ideas at a time!"
                    return
            elif self.action == "mind_read":
                time.sleep(0.5)
                if len(current_inventory) < 9:
                    i = 0
                    while i < 3:
                        choice = random.choice(nahidaCombatInventory)

                        if choice not in current_inventory:
                            current_inventory.append(choice)
                            message = "You read the mind of a random person!"
                            i += 1

                    if message != "You read the mind of a random person!":
                        message = "No minds were succesffuly read this time. :("
                return
            elif self.action == "conclusion":
                time.sleep(0.5)
                if len(xlCookingPot) == 3:
                    if check_recipe(xlCookingPot, valid_conclusions):
                        combatNahida.take_damage(100)

                        xlCookingPot.clear()
                        return
                    else:
                        message = "You cooked the wrong dish!"
                        turn = 'enemy'

                        xlCookingPot.clear()
                        return
                else:
                    message = "You need 3 ideas to come to a conclusion!"
                    return
            elif self.action == "radish":
                time.sleep(0.5)
                file = open("Dialogues/nahida_damage", "r")
                message = random.choice(file.readlines())
                if message.__contains__("10"):
                    current_scene.get_player().take_damage(10)
                if (current_scene.radishIndex < 6):
                    current_scene.radishIndex += 1
                    if current_scene.radishIndex == 6:
                        message = "You ran out of raidshes! A wild Kazuha appears!"
                        global radishAchievement
                        obtainAchievement(achievementList, "Way too many radishes")
                        radishAchievement = True
                file.close()
                return
            elif self.action == "fate_bound":
                current_scene.get_npc().take_damage(10)
                current_scene.emotional_damage(5)

                randomNum = random.randint(0, 5)

                messageFile = open("Dialogues/yelan_fatebound", "r")
                message = messageFile.readlines()[randomNum]
                messageFile.close()

                xiaoMessageFile = open("Dialogues/xiao_fatebound", "r")
                current_scene.xiao_message = xiaoMessageFile.readlines()[randomNum]
                xiaoMessageFile.close()

                time.sleep(0.5)
                turn = 'enemy'
                return
            elif self.action == "banish":
                if current_scene.get_npc().remaining_health < 50:
                    current_scene.get_npc().take_damage(100)

                    message = "Xiao braces for the final blow, seemingly surrendering to the shadows."
                    current_scene.xiao_message = "End it.. Release me from this torment."

                    time.sleep(0.5)
                    return
                else:
                    message = "Conqueror of Demons is too strong to be banished!"

                    turn = 'enemy'
                    time.sleep(0.5)
                    return
            elif self.action == "lament":
                current_scene.emotional_damage(-5 - current_scene.emotion)
                
                randomNum = random.randint(0, 2)

                if current_scene.emotion < 50:
                    messageFile = open("Dialogues/yelan_lament_low_emotion", "r")
                    message = messageFile.readlines()[randomNum]
                    messageFile.close()

                    xiaoMessageFile = open("Dialogues/xiao_lament_low_emotion", "r")
                    current_scene.xiao_message = xiaoMessageFile.readlines()[randomNum]
                    xiaoMessageFile.close()
                else:
                    messageFile = open("Dialogues/yelan_lament_high_emotion", "r")
                    message = messageFile.readlines()[randomNum]
                    messageFile.close()

                    xiaoMessageFile = open("Dialogues/xiao_lament_high_emotion", "r")
                    current_scene.xiao_message = xiaoMessageFile.readlines()[randomNum]
                    xiaoMessageFile.close()

                turn = 'enemy'
                time.sleep(0.5)
                return
            elif self.action == "mercy":
                if current_scene.emotion > 70:
                    current_scene.emotional_damage(-100)

                    randomNum = random.randint(0, 2)

                    messageFile = open("Dialogues/yelan_mercy", "r")
                    message = messageFile.readlines()[randomNum]
                    messageFile.close()

                    xiaoMessageFile = open("Dialogues/xiao_mercy", "r")
                    current_scene.xiao_message = xiaoMessageFile.readlines()[randomNum]
                    xiaoMessageFile.close()

                    time.sleep(0.5)
                    return
                else:
                    current_scene.emotional_damage(-10)

                    randomNum = random.randint(0, 2)

                    messageFile = open("Dialogues/yelan_mercy", "r")
                    message = messageFile.readlines()[randomNum]
                    messageFile.close()

                    xiaoMessageFile = open("Dialogues/xiao_mercy", "r")
                    current_scene.xiao_message = xiaoMessageFile.readlines()[randomNum]
                    xiaoMessageFile.close()

                    turn = 'enemy'
                    time.sleep(0.5)
                return

    def update(self):
        self.button_input()

def display_text(text):
    main_font = pygame.font.Font('Fonts/main_font.ttf', 25)
    color = '#47c0b4'
    padding = 10
    text_lines = wrap_text(text, main_font, 600 - padding * 2)  # Wrap text to fit within the chat box width

    y = 370  # Starting Y position within the chat box
    for line in text_lines:
        text_surface = main_font.render(line, False, color)
        screen.blit(text_surface, (20, y))
        y += 30  # Adjust Y position for the next line
        pygame.display.flip()

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_size = font.size(test_line)

        if test_size[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)
    return lines

def talk_npc(dialogue_path, background, character1_image, character2_image, character1_name, character2_name):
    main_font = pygame.font.Font('Fonts/main_font.ttf', 20)
    fopen = open(dialogue_path, "r")
    lines = fopen.readlines()
    fopen.close()

    current_line = 0
    while current_line < len(lines):
        if current_line % 2 == 0:
            screen.blit(pygame.image.load(background).convert_alpha(), (0, 0))

            yelan_dialogue = pygame.image.load(character1_image).convert_alpha()
            yelan_dialogue = pygame.transform.scale(yelan_dialogue, (150, 150))
            screen.blit(yelan_dialogue, (10, 180))

            name = pygame.draw.rect(screen, "#270023", (10, 335, 410, 25))

            character_name = main_font.render(character1_name, False, '#47c0b4')
            screen.blit(character_name, (25, 335))

            pygame.display.flip()
        else:
            screen.blit(pygame.image.load(background).convert_alpha(), (0, 0))
            ning_dialogue = pygame.image.load(character2_image).convert_alpha()
            ning_dialogue = pygame.transform.scale(ning_dialogue, (150, 150))
            screen.blit(ning_dialogue, (480, 180))

            name = pygame.draw.rect(screen, "#270023", (210, 335, 420, 25))
                
            character_name = main_font.render(character2_name, False, '#47c0b4')
            screen.blit(character_name, (225, 335))

            pygame.display.flip()
        line = lines[current_line]
        sentences = line.split('.')
        wait = True
        for sentence in sentences:
            str = sentence.strip()   
            wait = True               
            if str != "":
                text_box = pygame.draw.rect(screen, "#270023", (10, 365, 620, 100))
                display_text(str + '.')
                pygame.display.flip()
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                wait = False
                                break

        current_line += 1
        pygame.display.flip()
    reset_state()

def talk_multiple_npc(dialogue_path, background, character1_image, character2_image, character3_image, character1_name, character2_name, character3_name):
    main_font = pygame.font.Font('Fonts/main_font.ttf', 20)
    fopen = open(dialogue_path, "r")
    lines = fopen.readlines()
    fopen.close()

    current_line = 0
    while current_line < len(lines):
        screen.blit(pygame.image.load(background).convert_alpha(), (0, 0))

        if current_line % 3 == 0:
            # Display Character 1
            screen.blit(pygame.image.load(background).convert_alpha(), (0, 0))
            character_dialogue = pygame.image.load(character1_image).convert_alpha()
            character_dialogue = pygame.transform.scale(character_dialogue, (150, 150))
            screen.blit(character_dialogue, (10, 180))

            name = pygame.draw.rect(screen, "#270023", (10, 335, 410, 25))

            character_name = main_font.render(character1_name, False, '#47c0b4')
            screen.blit(character_name, (25, 335))

            pygame.display.flip()

        elif current_line % 3 == 1:
            # Display Character 2
            screen.blit(pygame.image.load(background).convert_alpha(), (0, 0))
            character_dialogue = pygame.image.load(character2_image).convert_alpha()
            character_dialogue = pygame.transform.scale(character_dialogue, (150, 150))
            screen.blit(character_dialogue, (10, 180))

            name = pygame.draw.rect(screen, "#270023", (10, 335, 410, 25))

            character_name = main_font.render(character2_name, False, '#47c0b4')
            screen.blit(character_name, (25, 335))

            pygame.display.flip()

        else:
            # Display Character 3
            screen.blit(pygame.image.load(background).convert_alpha(), (0, 0))
            character_dialogue = pygame.image.load(character3_image).convert_alpha()
            character_dialogue = pygame.transform.scale(character_dialogue, (150, 150))
            screen.blit(character_dialogue, (480, 180))

            name = pygame.draw.rect(screen, "#270023", (210, 335, 420, 25))
                
            character_name = main_font.render(character3_name, False, '#47c0b4')
            screen.blit(character_name, (225, 335))

            pygame.display.flip()

        line = lines[current_line]
        sentences = line.split('.')
        wait = True
        for sentence in sentences:
            str = sentence.strip()
            wait = True
            if str != "":
                text_box = pygame.draw.rect(screen, "#270023", (10, 365, 620, 100))
                display_text(str + '.')
                pygame.display.flip()
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                wait = False
                                break

        current_line += 1
        pygame.display.flip()
    reset_state()

class Ning_npc(Npc):
    background = 'Backgrounds/jade_chamber_bg1.png'
    character1_image = 'Dialogue_Images/yelan_ning_dialogue.png'
    character1_name = 'Yelan'
    character2_name = 'Ningguang, Lady of the Jade Chamber'
    def talk(self):
        talk_npc(self.dialogue_path, self.background, self.character1_image, self.npc_image, self.character1_name, self.character2_name)
        
        global artifactInventory, ningAchievement
        itemsToObtain = ["Odyssean Flower", "Wicked Mage's Plumule", "Nymph's Constancy", "Heroes' Tea Party", "Fell Dragon's Monocle"]
        for item in itemsToObtain:
            obtainItem(artifactInventory, item)
        
        obtainAchievement(achievementList, "Not again")
        ningAchievement = True

class Ganyu_npc(Npc):
    background = 'Backgrounds/yelan_ganyu_dialogue.png'
    character1_image = 'Dialogue_Images/yelan_ganyu_dialogue.png'
    character1_name = 'Yelan'
    character2_name = 'Ganyu, Secretary of the Yuehai Pavilion'
    background2 = 'Backgrounds/yelan_xl_dialogue.png'
    dialogue_path2 = 'Dialogues/yelan_ganyu_liyue_street'

    def talk(self):
        talk_npc(self.dialogue_path, self.background, self.npc_image, self.character1_image, self.character2_name, self.character1_name)
        talk_npc(self.dialogue_path2, self.background2, self.npc_image, self.character1_image, self.character2_name, self.character1_name)

        global current_scene, ganyuAchievement, specialInventory
        current_scene = LiyueStreetScene(player, screen, xlNpc)
        player.rect.x = 0
        player.image = pygame.transform.flip(player.image, True, False)
        player.direction = "right"

        obtainAchievement(achievementList, "Let it snow")
        obtainItem(specialInventory, "Qingxin")
        ganyuAchievement = True
   
class Xiangling_npc(Npc):
    background = 'Backgrounds/yelan_xl_dialogue.png'
    character1_image = 'Dialogue_Images/yelan_ganyu_dialogue.png'
    character1_name = 'Yelan'
    character2_name = 'Xiangling, Chef de Cuisine'
    dialogue_path_post_combat = 'Dialogues/yelan_xiangling_post-combat'

    def talk(self):
        global xlCombat, xlAchievement, specialInventory
        global current_scene, current_inventory, inventory_lock, achievement_lock, xlCombatInventoryCopy
        if xlCombat == False:
            talk_npc(self.dialogue_path, self.background, self.character1_image, self.npc_image, self.character1_name, self.character2_name)
            xlCombat = True
            current_inventory = copy.deepcopy(xlCombatInventory)
            inventory_lock, achievement_lock = True, True
            current_scene = YelanXlCombat(combatYelan, screen, combatXl)
        else:
            global xlDialogue
            talk_npc(xlDialogue, self.background, self.npc_image, self.character1_image, self.character2_name, self.character1_name)

            xlCombat = False
            current_inventory = defaultInventory
            obtainAchievement(achievementList, "Adeptus' Temptation")
            obtainItem(specialInventory, "Dango")
            xlAchievement = True

class LaylaNpc(Npc):
    background = 'Backgrounds/less_foresty.png'
    character1_name = 'Layla, Star Gazer'
    character2_name = 'Yelan'
    character2_image = 'Dialogue_Images/yelan_layla_dialogue.png'
    background2 = 'Backgrounds/yelan_alhaitham_dialogue.png'
    dialogue_path2 = 'Dialogues/yelan_layla_alhaitham_spot'
    flipped_npc_image = 'Dialogue_Images/layla_dialogue_flipped.png'
    flipped_character2_image = 'Dialogue_Images/yelan_layla_dialogue_flipped.png'

    def talk(self):
        talk_npc(self.dialogue_path, self.background, self.character2_image, self.npc_image, self.character2_name, self.character1_name)
        talk_npc(self.dialogue_path2, self.background2, self.flipped_npc_image, self.flipped_character2_image, self.character1_name, self.character2_name)

        global current_scene, laylaAchievement
        current_scene = YelanAlhaithamScene(player, screen, alhaithamNpc)
        player.rect.x = 500
        obtainAchievement(achievementList, "Half-awake, half-asleep")
        laylaAchievement = True

class AlhaithamNpc(Npc):
    background = 'Backgrounds/yelan_alhaitham_dialogue.png'
    character2_image = 'Dialogue_Images/yelan_alhaitham_dialogue.png'
    character2_name = 'Yelan'
    character1_name = 'Alhaitham, Acting Grand Sage'
    def talk(self):
        talk_npc(self.dialogue_path, self.background, self.npc_image, self.character2_image, self.character1_name, self.character2_name)

        global alhaithamAchievement, yelanLoveAchievement
        obtainAchievement(achievementList, "A dance with imperfection")
        obtainAchievement(achievementList, "Serendipitous Symphony")
        alhaithamAchievement = True
        yelanLoveAchievement = True

class NahidaNpc(Npc):
    background = 'Backgrounds/yelan_nahida_dialogue.png'
    character1_image = 'Dialogue_Images/yelan_nahida_dialogue.png'
    character1_name = 'Yelan'
    character2_name = 'Nahida, Lesser Lord Kusanali'
    dialogue_path_post_combat = "Dialogues/yelan_nahida_post-combat"

    def talk(self):
        global nahidaCombat, current_scene, current_inventory, inventory_lock, achievement_lock, nahidaAchievement, specialInventory
        if nahidaCombat == False:
            talk_npc(self.dialogue_path, self.background, self.character1_image, self.npc_image, self.character1_name, self.character2_name)

            nahidaCombat = True
            current_inventory = []
            inventory_lock, achievement_lock = True, True
            current_scene = YelanNahidaCombat(combatYelan, screen, combatNahida)
        else:
            talk_npc(self.dialogue_path_post_combat, self.background, self.npc_image, self.character1_image, self.character2_name, self.character1_name)

            nahidaCombat = False
            current_inventory = defaultInventory
            obtainAchievement(achievementList, "Swinging in the realm of the Divine")
            obtainItem(specialInventory, "Rukkhadevata's Bell")
            nahidaAchievement = True

class AmberColleiNpc(Npc):
    background = 'Backgrounds/amber_collei_dialogue.png'
    character2_image = 'Dialogue_Images/collei_dialogue.png'
    character3_image = 'Dialogue_Images/yelan_amber_collei_dialogue.png'
    character1_name = 'Amber, Knights of Favonius Outrider'
    character2_name = 'Collei, Avidya Forest Ranger Trainee'
    character3_name = 'Yelan'
    
    def talk(self):
        talk_multiple_npc(self.dialogue_path, self.background, self.character2_image, self.npc_image, self.character3_image, self.character2_name, self.character1_name, self.character3_name)
        global amberColleiAchievement
        obtainAchievement(achievementList, "A bridge between Nations")
        amberColleiAchievement = True

class XiaoNpc(Npc):
    background = 'Backgrounds/yelan_xiao_dialogue.png'
    character1_image = 'Dialogue_Images/yelan_xiao_dialogue.png'
    character1_image_post_combat = 'Dialogue_Images/yelan_xiao_post-combat.png'
    character1_name = 'Yelan'
    character2_name = 'Xiao, Vigilant Yaksha'
    character2_image_post_combat = 'Dialogue_Images/xiao_post_dialogue.png'
    dialogue_path_post_combat = 'Dialogues/yelan_xiao_post-combat'

    def talk(self):
        global xiaoCombat, xiaoAchievement
        global current_scene, current_inventory, inventory_lock, achievement_lock, xiaoCombatInventoryCopy
        if xiaoCombat == False:
            talk_npc(self.dialogue_path, self.background, self.npc_image, self.character1_image, self.character2_name, self.character1_name)

            xiaoCombat = True
            inventory_lock, achievement_lock = True, True
            current_inventory = []
            current_scene = YelanXiaoCombat(combatYelan, screen, combatXiao)
        else:
            talk_npc(self.dialogue_path_post_combat, self.background, self.character1_image_post_combat, self.character2_image_post_combat, self.character1_name, self.character2_name)
            
            xiaoCombat = False
            current_inventory = defaultInventory
            obtainAchievement(achievementList, "Dispel the Evil")
            xiaoAchievement = True

class ZhongliNpc(Npc):
    background = 'Backgrounds/yelan_zhongli_dialogue.png'
    character1_image = 'Dialogue_Images/yelan_zhongli_dialogue.png'
    character1_name = 'Yelan'
    character2_name = 'Zhongli, Funeral Parlor Consultant'
    def talk(self):
        talk_npc(self.dialogue_path, self.background, self.character1_image, self.npc_image, self.character1_name, self.character2_name)

        global zhongliAchievement, specialInventory
        obtainAchievement(achievementList, "Osmanthus wine tastes the same as I remember…")
        obtainItem(specialInventory, "Osmanthus Wine")
        zhongliAchievement = True

class dendroSlimeCombat(Scene):
    def __init__(self, player, screen, Slime):
        super().__init__(player, screen, Slime)
        self.background = pygame.image.load('Backgrounds/dendro_slime_combat.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        global turn 
        turn = "player"
        global message
        message = "Choose an action"

    def display(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        if self.npc:
            self.npc.rect.x = 450
            self.npc.rect.y = 50
            self.npc.draw(self.screen)
            self.npc.update()
            self.npc.rect.x = 320
            self.npc.rect.y = 320

        self.player.draw(self.screen)
        self.player.update()

        bar_scale = 200 // self.player.max_health
        # Draw player health bar
        for i in range(self.player.max_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
            
        for i in range(self.player.remaining_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
            
        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.player.remaining_health} / {self.player.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = width - 10 - text_rect.width
        text_rect.y = height - 120
        screen.blit(text, text_rect)

        # Draw enemy health bar
        for i in range(self.npc.max_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
        
        for i in range(self.npc.remaining_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
        
        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.npc.remaining_health} / {self.npc.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 25
        screen.blit(text, text_rect)

        # draw text box
        pygame.draw.rect(screen, (0, 0, 0), (5, height - 95, width - 10, 90))
        pygame.draw.rect(screen, (255, 203, 164), (10, height - 90, width - 20, 80))

        # draw decision buttons
        button_y = 392
        button_x = 540
        i = 0
        for button in combat_button_group:
            screen.blit(button.image, (button_x - (80 * (i % 2)), button_y + (40 * (i // 2))))
            i = i + 1

        message_lines = textwrap.wrap(message, width=52)
        for i, line in enumerate(message_lines):
            line_text = font.render(line, True, (0, 0, 0))
            # line_rect = line_text.get_rect()
            text_rect = line_text.get_rect()
            text_rect.x = 20
            text_rect.y = height - 80 + i * 20
            screen.blit(line_text, text_rect)

        pygame.display.flip()
    
    def fight(self):
        if self.player.remaining_health <= 0:
            # button_group.sprites()[0].start_game = False
            global current_scene, turn, inventory_lock, achievement_lock, talking
            current_scene = OvergrownArea(player, screen, None)
            talking = False
            self.player.remaining_health = self.player.max_health
            self.npc.remaining_health = self.npc.max_health
            inventory_lock, achievement_lock = False, False
            turn = "player"
        if self.npc.remaining_health <= 0:
            # global current_scene, turn, inventory_lock, achievement_lock
            self.npc.remaining_health = self.npc.max_health
            current_scene = OvergrownArea(player, screen, None)
            talking = False
            self.player.remaining_health = self.player.max_health
            inventory_lock, achievement_lock = False, False
            turn = "player"
        if (turn == "player"):
            combat_button_group.update()
        else:
            self.player.take_damage(self.npc.attack)
            turn = "player"
            global message
            message = "The slime attacked you for " + str(self.npc.attack) + " damage!"
            time.sleep(0.5)

    def update(self):
        self.display()
        self.fight()

class geoSlimeCombat(Scene):
    def __init__(self, player, screen, Slime):
        super().__init__(player, screen, Slime)
        self.background = pygame.image.load('Backgrounds/geo_slime_combat.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        global turn 
        turn = "player"
        global message
        message = "Choose an action"

    def display(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        if self.npc:
            self.npc.rect.x = 450
            self.npc.rect.y = 50
            self.npc.draw(self.screen)
            self.npc.update()
            self.npc.rect.x = 320
            self.npc.rect.y = 320

        self.player.draw(self.screen)
        self.player.update()

        bar_scale = 200 // self.player.max_health
        # Draw player health bar
        for i in range(self.player.max_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
            
        for i in range(self.player.remaining_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
            
        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.player.remaining_health} / {self.player.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = width - 10 - text_rect.width
        text_rect.y = height - 120
        screen.blit(text, text_rect)

        # Draw enemy health bar
        for i in range(self.npc.max_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
        
        for i in range(self.npc.remaining_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
        
        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.npc.remaining_health} / {self.npc.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 25
        screen.blit(text, text_rect)

        # draw text box
        pygame.draw.rect(screen, (0, 0, 0), (5, height - 95, width - 10, 90))
        pygame.draw.rect(screen, (255, 203, 164), (10, height - 90, width - 20, 80))

        # draw decision buttons
        button_y = 392
        button_x = 540
        i = 0
        for button in combat_button_group:
            screen.blit(button.image, (button_x - (80 * (i % 2)), button_y + (40 * (i // 2))))
            i = i + 1

        message_lines = textwrap.wrap(message, width=52)
        for i, line in enumerate(message_lines):
            line_text = font.render(line, True, (0, 0, 0))
            # line_rect = line_text.get_rect()
            text_rect = line_text.get_rect()
            text_rect.x = 20
            text_rect.y = height - 80 + i * 20
            screen.blit(line_text, text_rect)

        pygame.display.flip()
    
    def fight(self):
        if self.player.remaining_health <= 0:
            # button_group.sprites()[0].start_game = False
            global current_scene, turn, inventory_lock, achievement_lock, talking
            current_scene = WangshuInnRoad(player, screen, None)
            talking = False
            self.player.remaining_health = self.player.max_health
            self.npc.remaining_health = self.npc.max_health
            inventory_lock, achievement_lock = False, False
            turn = "player"
        if self.npc.remaining_health <= 0:
            # global current_scene, turn, inventory_lock, achievement_lock
            self.npc.remaining_health = self.npc.max_health
            current_scene = WangshuInnRoad(player, screen, None)
            talking = False
            self.player.remaining_health = self.player.max_health
            inventory_lock, achievement_lock = False, False
            turn = "player"
        if (turn == "player"):
            combat_button_group.update()
        else:
            self.player.take_damage(self.npc.attack)
            turn = "player"
            global message
            message = "The slime attacked you for " + str(self.npc.attack) + " damage!"
            time.sleep(0.5)

    def update(self):
        self.display()
        self.fight()

class YelanXlCombat(Scene):
    def __init__(self, player, screen, combatXl):
        super().__init__(player, screen, combatXl)
        self.background = pygame.image.load('Backgrounds/xl_combat_bg.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        global turn 
        turn = "player"
        global message
        message = "Choose an action"
        self.goubaIndex = 0
        self.goubaPaths = open("Dialogues/goubaPaths", "r")
        self.goubaPathsArray = self.goubaPaths.readlines()
        self.goubaPaths.close()


    def display(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        if self.npc:
            self.npc.draw(self.screen)
            self.npc.update()

        self.player.draw(self.screen)
        self.player.update()

        bar_scale = 200 // self.player.max_health
        # Draw player health bar
        for i in range(self.player.max_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
            
        for i in range(self.player.remaining_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
            
        # display "SATIETY" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'SATIETY: {self.player.remaining_health} / {self.player.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = width - 10 - text_rect.width
        text_rect.y = height - 120
        screen.blit(text, text_rect)

        # Draw enemy health bar
        for i in range(self.npc.max_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
        
        for i in range(self.npc.max_health - self.npc.remaining_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
        
        # display "HUNGER" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HUNGER: {self.npc.remaining_health} / {self.npc.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 25
        screen.blit(text, text_rect)

        # draw text box
        pygame.draw.rect(screen, (0, 0, 0), (5, height - 95, width - 10, 90))
        pygame.draw.rect(screen, (255, 203, 164), (10, height - 90, width - 20, 80))

        # draw decision buttons
        button_y = 392
        button_x = 540
        i = 0
        for button in xl_combat_button_group:
            screen.blit(button.image, (button_x - (80 * (i % 2)), button_y + (40 * (i // 2))))
            i = i + 1

        message_lines = textwrap.wrap(message, width=52)
        for i, line in enumerate(message_lines):
            line_text = font.render(line, True, (0, 0, 0))
            # line_rect = line_text.get_rect()
            text_rect = line_text.get_rect()
            text_rect.x = 20
            text_rect.y = height - 80 + i * 20
            screen.blit(line_text, text_rect)

        # display the gouba
        goubaOffset = 0
        for i in range(self.goubaIndex):
            gouba = pygame.image.load(self.goubaPathsArray[i].strip()).convert_alpha()
            gouba = pygame.transform.scale(gouba, (60, 60))
            screen.blit(gouba, (20 + goubaOffset, 50))
            goubaOffset += 70

        pygame.display.flip()
    
    def fight(self):
        if self.player.remaining_health <= 0:
            global current_scene, xlCookingPot, turn, inventory_lock, achievement_lock, xlCombatInventoryCopy, xlCombat
            xlCombat = False
            current_scene = LiyueStreetScene(player, screen, xlNpc)
            self.player.remaining_health = self.player.max_health
            xlCookingPot.clear()
            self.npc.remaining_health = self.npc.max_health
        if self.npc.remaining_health <= 0:
            current_scene = LiyueStreetScene(player, screen, xlNpc)
            xlCookingPot.clear()
            self.npc.remaining_health = self.npc.max_health
            turn = "player"
            global xlCombatInventory
            xlCombatInventory = copy.deepcopy(xlCombatInventoryCopy)
            self.player.remaining_health = self.player.max_health
            inventory_lock, achievement_lock = False, False
        if (turn == "player"):
            xl_combat_button_group.update()
        else:
            self.player.take_damage(self.npc.attack)
            turn = "player"
            global message
            file = open("Dialogues/xl_damage", "r")
            message = random.choice(file.readlines())

    def update(self):
        self.display()
        self.fight()

class YelanNahidaCombat(Scene):
    def __init__(self, player, screen, combatNahida):
        super().__init__(player, screen, combatNahida)
        self.background = pygame.image.load('Backgrounds/nahida_combat_bg.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        global turn 
        turn = "player"
        global message
        message = "Choose an action"
        self.radishIndex = 0
        radishPaths = open("Dialogues/radishPaths", "r")
        self.radishPathsArray = radishPaths.readlines()
        radishPaths.close()

    def display(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        if self.npc:
            self.npc.draw(self.screen)
            self.npc.update()

        self.player.draw(self.screen)
        self.player.update()

        bar_scale = 200 // self.player.max_health
        # Draw player health bar
        for i in range(self.player.max_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
            
        for i in range(self.player.remaining_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
            
        # display "CONFUSION" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'CONFUSION: {self.player.remaining_health} / {self.player.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = width - 10 - text_rect.width
        text_rect.y = height - 120
        screen.blit(text, text_rect)

        # Draw enemy health bar
        for i in range(self.npc.max_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
        
        for i in range(self.npc.remaining_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
        
        # display "INSIGHT" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'INSIGHT: {self.npc.remaining_health} / {self.npc.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 25
        screen.blit(text, text_rect)

        # draw text box
        pygame.draw.rect(screen, (0, 0, 0), (5, height - 95, width - 10, 90))
        pygame.draw.rect(screen, (255, 203, 164), (10, height - 90, width - 20, 80))

        # draw decision buttons
        button_y = 392
        button_x = 540
        i = 0
        for button in nahida_combat_button_group:
            screen.blit(button.image, (button_x - (80 * (i % 2)), button_y + (40 * (i // 2))))
            i = i + 1

        message_lines = textwrap.wrap(message, width=52)
        for i, line in enumerate(message_lines):
            line_text = font.render(line, True, (0, 0, 0))
            # line_rect = line_text.get_rect()
            text_rect = line_text.get_rect()
            text_rect.x = 20
            text_rect.y = height - 80 + i * 20
            screen.blit(line_text, text_rect)

        # display the radish
        radishOffset = 0
        for i in range(self.radishIndex):
            radish = pygame.image.load(self.radishPathsArray[i].strip()).convert_alpha()
            radish = pygame.transform.scale(radish, (60, 60))
            screen.blit(radish, (20 + radishOffset, 50))
            radishOffset += 70

        pygame.display.flip()
    
    def fight(self):
        if self.player.remaining_health <= 0:
            global current_scene, xlCookingPot, turn, inventory_lock, achievement_lock, xlCombatInventoryCopy, nahidaCombat
            nahidaCombat = False
            current_scene = YelanNahidaScene(player, screen, nahidaNpc)
            self.player.remaining_health = self.player.max_health
            xlCookingPot.clear()
            self.npc.remaining_health = self.npc.max_health
        if self.npc.remaining_health <= 0:
            current_scene = YelanNahidaScene(player, screen, nahidaNpc)
            xlCookingPot.clear()
            self.npc.remaining_health = self.npc.max_health
            turn = "player"
            self.player.remaining_health = self.player.max_health
            inventory_lock, achievement_lock = False, False
        if (turn == "player"):
            nahida_combat_button_group.update()
        else:
            self.player.take_damage(self.npc.attack)
            turn = "player"
            global message
            file = open("Dialogues/nahida_damage", "r")
            message = random.choice(file.readlines())

    def update(self):
        self.display()
        self.fight()

class YelanXiaoCombat(Scene):
    def __init__(self, player, screen, combatNahida):
        super().__init__(player, screen, combatNahida)
        self.background = pygame.image.load('Backgrounds/xiao_combat_bg.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        global turn 
        turn = "player"
        global message
        message = "Choose an action"
        self.emotion = 0
        self.max_emotion = 100
        self.xiao_message = "Come at me, fool!"

    def display(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        if self.npc:
            self.npc.draw(self.screen)
            self.npc.update()

        self.player.draw(self.screen)
        self.player.update()

        bar_scale = 200 // self.player.max_health
        # Draw player health bar
        for i in range(self.player.max_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
            
        for i in range(self.player.remaining_health):
            bar = (width - 10 - bar_scale * i, height - 125, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
            
        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.player.remaining_health} / {self.player.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = width - 10 - text_rect.width
        text_rect.y = height - 120
        screen.blit(text, text_rect)

        # Draw enemy health bar
        for i in range(self.npc.max_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (200, 0, 0), bar)
        
        for i in range(self.npc.remaining_health):
            bar = (10 + bar_scale * i, 20, bar_scale, 23)
            pygame.draw.rect(screen, (0, 200, 0), bar)
        
        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.npc.remaining_health} / {self.npc.max_health}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 25
        screen.blit(text, text_rect)

        # Draw enemy emotion bar        
        for i in range(self.max_emotion):
            bar = (10 + bar_scale * i, 50, bar_scale, 23)
            pygame.draw.rect(screen, (48, 139, 130), bar)

        for i in range(self.emotion):
            if i >= 100:
                break
            else:
                bar = (10 + bar_scale * i, 50, bar_scale, 23)
                pygame.draw.rect(screen, "#47c0b4", bar)

        # display EMOTION text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'EMOTION: {self.emotion} / {self.max_emotion}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 55
        screen.blit(text, text_rect)

        # draw text box
        pygame.draw.rect(screen, (0, 0, 0), (5, height - 95, width - 10, 90))
        pygame.draw.rect(screen, (255, 203, 164), (10, height - 90, width - 20, 80))

        # # draw enemy text box
        pygame.draw.rect(screen, (0, 0, 0), (5, 80, 3 * width / 4 - 25, 90))
        pygame.draw.rect(screen, "#73beb0", (10, 85, 3 * width / 4 - 35, 80))

        # draw decision buttons
        button_y = 392
        button_x = 540
        i = 0
        for button in xiao_combat_button_group:
            screen.blit(button.image, (button_x - (80 * (i % 2)), button_y + (40 * (i // 2))))
            i = i + 1

        message_lines = textwrap.wrap(message, width=52)
        for i, line in enumerate(message_lines):
            line_text = font.render(line, True, (0, 0, 0))
            text_rect = line_text.get_rect()
            text_rect.x = 20
            text_rect.y = height - 80 + i * 20
            screen.blit(line_text, text_rect)

        message_lines = textwrap.wrap(self.xiao_message, width=52)
        for i, line in enumerate(message_lines):
            line_text = font.render(line, True, (0, 0, 0))
            text_rect = line_text.get_rect()
            text_rect.x = 20
            text_rect.y = 90 + i * 20
            screen.blit(line_text, text_rect)

        pygame.display.flip()
    
    def fight(self):
        if self.player.remaining_health <= 0:
            global current_scene, xlCookingPot, turn, inventory_lock, achievement_lock, xlCombatInventoryCopy, xiaoCombat
            xiaoCombat = False
            current_scene = YelanXiaoScene(player, screen, xiaoNpc)
            self.player.remaining_health = self.player.max_health
            xlCookingPot.clear()
            self.npc.remaining_health = self.npc.max_health
        if self.npc.remaining_health <= 0 or self.emotion >= self.max_emotion:
            time.sleep(1)
            current_scene = YelanXiaoScene(player, screen, xiaoNpc)
            xlCookingPot.clear()
            self.npc.remaining_health = self.npc.max_health
            turn = "player"
            self.player.remaining_health = self.player.max_health
            inventory_lock, achievement_lock = False, False
        if (turn == "player"):
            xiao_combat_button_group.update()
        else:
            self.player.take_damage(self.npc.attack)
            turn = "player"
        
    def emotional_damage(self, damage):
        self.emotion -= damage
        if self.emotion < 0:
            self.emotion = 0

    def update(self):
        self.display()
        self.fight()

class YelanNahidaScene(Scene):
    def __init__(self, player, screen, nahidaNpc):
        super().__init__(player, screen, nahidaNpc)
        self.background = pygame.image.load('Backgrounds/yelan_nahida_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = NahidaPalace(player, screen)
        
    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class NahidaPalace(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/nahida_palace.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

        door_x = 360
        door_y = height // 2
        door_width = 50
        door_height = 20
        self.invisible_door = pygame.Rect(door_x, door_y, door_width, door_height)

    def transition(self):
        global current_scene

        if player.rect.colliderect(self.invisible_door):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                player.rect.x = 0
                player.rect.y = 330
                current_scene = YelanNahidaScene(player, screen, nahidaNpc)
                return

        elif player.rect.x <= -30:
            player.rect.x = 490
            current_scene = RiverTrees(player, screen)

class RiverTrees(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/river_trees.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

        door_x = 20
        door_y = height // 2
        door_width = 50
        door_height = 20
        self.invisible_door = pygame.Rect(door_x, door_y, door_width, door_height)

    def transition(self):
        global current_scene

        if player.rect.colliderect(self.invisible_door):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                player.rect.x = 0
                player.rect.y = 330
                current_scene = NahidaPalace(player, screen)
                return
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = AlcazarzarayPalace(player, screen)

class AlcazarzarayPalace(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/alcazarzaray_palace.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = RiverTrees(player, screen)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = YelanAlhaithamScene(player, screen, alhaithamNpc)

class YelanAlhaithamScene(Scene):
    def __init__(self, player, screen, alhaithamNpc):
        super().__init__(player, screen, alhaithamNpc)
        self.background = pygame.image.load('Backgrounds/yelan_alhaitham_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = AlcazarzarayPalace(player, screen)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = LessForesty(player, screen, laylaNpc)

    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class LessForesty(Scene):
    def __init__(self, player, screen, laylaNpc):
        super().__init__(player, screen, laylaNpc)
        self.background = pygame.image.load('Backgrounds/less_foresty.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = YelanAlhaithamScene(player, screen, alhaithamNpc)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = AmberColleiScene(player, screen, amberColleiNpc)

    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class AmberColleiScene(Scene):
    def __init__(self, player, screen, amberColleiNpc):
        super().__init__(player, screen, amberColleiNpc)
        self.background = pygame.image.load('Backgrounds/amber_collei_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = LessForesty(player, screen, laylaNpc)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = OvergrownArea(player, screen, combatSlime)
    
    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class OvergrownArea(Scene):
    def __init__(self, player, screen, npc):
        super().__init__(player, screen, npc)
        self.background = pygame.image.load('Backgrounds/overgrown_area.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = AmberColleiScene(player, screen, amberColleiNpc)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = YelanGanyuScene(player, screen, ganyu_npc) # thinking about it

    def talk_npc(self):
        global talking
        if self.get_npc() != None:
            if player.rect.colliderect(self.get_npc().get_rect()):
                global current_scene
                current_scene = dendroSlimeCombat(combatYelan, screen, combatSlime)

class LiyueHarbor(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/beidou_kazuha_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = LiyueStreetScene(player, screen, xlNpc)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = LiyueHarbor(player, screen)

class LakeTransition(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/lake_transition.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = YelanGanyuScene(player, screen, ganyu_npc)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = LiyueStreetScene(player, screen, xlNpc)

class LiyueStreetScene(Scene):
    def __init__(self, player, screen, xlNpc):
        super().__init__(player, screen, xlNpc)
        self.background = pygame.image.load('Backgrounds/yelan_xl_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = LakeTransition(player, screen)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = LiyueHarbor(player, screen)

    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class YelanXiaoScene(Scene):
    def __init__(self, player, screen, xiaoNpc):
        super().__init__(player, screen, xiaoNpc)
        self.background = pygame.image.load('Backgrounds/yelan_xiao_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            player.rect.x = 490
            global current_scene
            current_scene = YelanZhongliScene(player, screen, zhongliNpc)

    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class YelanZhongliScene(Scene):
    def __init__(self, player, screen, zhongliNpc):
        super().__init__(player, screen, zhongliNpc)
        self.background = pygame.image.load('Backgrounds/yelan_zhongli_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

        self.teacup_image = pygame.image.load('Images/teacup.png').convert_alpha()
        self.teacup_image = pygame.transform.scale(self.teacup_image, (20, 50))
    
    def display(self):
        screen.blit(self.background, (0, 0))

        teacup_rect = pygame.Rect(width / 3, 285, 20, 50)
        screen.blit(self.teacup_image, teacup_rect.topleft)

        if player.rect.colliderect(teacup_rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                global zhongliVisible
                zhongliVisible = True
        
        if zhongliVisible == True:
            zhongliNpc.draw(screen)
            zhongliNpc.update()
        
        player.draw(screen)
        player.update()
            
    def transition(self):
        global current_scene

        if player.rect.y <= 0:
            player.rect.y = 320
            current_scene = YelanXiaoScene(player, screen, xiaoNpc)

        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = WangshuInnRoad(player, screen, combatGeoSlime)

    def talk_npc(self):
        global talking
        if talking == True and zhongliVisible == True:
            self.npc.talk()

class WangshuInnRoad(Scene):
    def __init__(self, player, screen, slime):
        super().__init__(player, screen, slime)
        self.background = pygame.image.load('Backgrounds/wangshu_inn_road.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        global current_scene

        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = YelanZhongliScene(player, screen, zhongliNpc)
        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = LiyueFlowersScene(player, screen)

    def talk_npc(self):
        global talking
        if self.get_npc() != None:
            if player.rect.colliderect(self.get_npc().get_rect()):
                global current_scene
                current_scene = geoSlimeCombat(combatYelan, screen, combatGeoSlime)

class LiyueFlowersScene(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/liyue_flower_scene.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

        self.flowers = pygame.image.load('Inventory/special/spider_lily.png').convert_alpha()
        self.flowers = pygame.transform.scale(self.flowers, (50, 50))

    def display(self):
        screen.blit(self.background, (0, 0))

        flower_rect = pygame.Rect(width / 4 - 30, 265, 100, 160)
        screen.blit(self.flowers, flower_rect.topleft)

        player.draw(screen)
        player.update()

        pygame.display.flip()

    def transition(self):
        global current_scene

        if player.rect.x <= -30: 
            player.rect.x = 490
            current_scene = WangshuInnRoad(player, screen, combatGeoSlime)
        if player.rect.x >= 640:
            player.rect.x = 0
            current_scene = YelanGanyuScene(player, screen, ganyu_npc)

        flower_rect = pygame.Rect(width / 4 - 30, 265, 100, 160)
        if player.rect.colliderect(flower_rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                global specialInventory
                obtainItem(specialInventory, "Spider Lily")

class YelanGanyuScene(Scene):
    def __init__(self, player, screen, ganyu_npc):
        super().__init__(player, screen, ganyu_npc)
        self.background = pygame.image.load('Backgrounds/yelan_ganyu_dialogue.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = LiyueFlowersScene(player, screen)

        elif player.rect.x >= 640:
            player.rect.x = 0
            current_scene = LakeTransition(player, screen)
        
        elif player.rect.y <= 0:
            player.rect.y = 320
            current_scene = OvergrownArea(player, screen, combatSlime)

    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

class JadeChamberBalcony(Scene):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.background = pygame.image.load('Backgrounds/jade_chamber_balcony.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        
        self.balloon_image = pygame.image.load('Images/balloon.png').convert_alpha()
        self.balloon_image = pygame.transform.scale(self.balloon_image, (100, 160))

    def display(self):
        screen.blit(self.background, (0, 0))

        balloon_rect = pygame.Rect(400, 180, 100, 160)
        screen.blit(self.balloon_image, balloon_rect.topleft)

        player.draw(screen)
        player.update()

    def transition(self):
        if player.rect.x <= -30:
            global current_scene
            player.rect.x = 490
            current_scene = YelanNingScene(player, screen, ning_npc)

        balloon_rect = pygame.Rect(400, 180, 75, 150)
        if player.rect.colliderect(balloon_rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                player.rect.x = 490
                current_scene = YelanGanyuScene(player, screen, ganyu_npc)

class YelanNingScene(Scene):
    def __init__(self, player, screen, ning_npc):
        super().__init__(player, screen, ning_npc)
        self.background = pygame.image.load('Backgrounds/jade_chamber_bg1.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))

    def talk_npc(self):
        global talking
        if talking == True:
            self.npc.talk()

    def transition(self):
        if self.player.rect.x >= 640:
            global current_scene
            self.player.rect.x = 0
            current_scene = JadeChamberBalcony(player, self.screen)

def reset_state():
    global talking
    talking = False

def show_inventory(item_images):
    global inventory_toggle

    # Box dimensions and layout
    box_width, box_height = 80, 80
    box_outline_thickness = 1
    box_spacing = 18
    num_boxes_per_row = 6
    num_rows = 4

    font = pygame.font.Font(pygame.font.get_default_font(), 18)  # Use a default font for simplicity
    title_text = font.render("Inventory", True, "#47c0b4")
    title_rect = title_text.get_rect(topleft=(10, 10))

    while inventory_toggle:
        # Draw background
        screen.fill((39, 0, 35))

        # Draw title
        screen.blit(title_text, title_rect)

        # Draw boxes with item images
        for index, (image_path, item_name, item_description, *optional) in enumerate(item_images):
            if optional and optional[0].get("aquired", False) is False:
                continue
            
            row = index // num_boxes_per_row
            col = index % num_boxes_per_row

            x = col * (box_width + box_spacing) + (width - (num_boxes_per_row * (box_width + box_spacing))) // 2
            y = row * (box_height + box_spacing) + (height - (num_rows * (box_height + box_spacing))) // 2 + 20

            # Load image
            item_image = pygame.image.load(image_path)
            item_image = pygame.transform.scale(item_image, (box_width, box_height))

            # Draw image on the screen
            screen.blit(item_image, (x, y))

        pygame.display.update()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                inventory_toggle = not inventory_toggle
                break
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                game_loop = False
                pygame.quit()
                quit()

            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if any item is clicked
                for index, (image_path, item_name, item_description, *optional) in enumerate(item_images):
                    if optional and optional[0].get("aquired", False) is False:
                        continue
                    
                    row = index // num_boxes_per_row
                    col = index % num_boxes_per_row

                    x = col * (box_width + box_spacing) + (width - (num_boxes_per_row * (box_width + box_spacing))) // 2
                    y = row * (box_height + box_spacing) + (height - (num_rows * (box_height + box_spacing))) // 2 + 20

                    # Check if the mouse click is inside the item box
                    if x <= mouse_x <= x + box_width and y <= mouse_y <= y + box_height:
                        # Show item details
                        display_item_details(item_images, index)

def display_item_details(item_images, index):
    # Box dimensions and layout
    box_width, box_height = 420, 220
    box_outline_thickness = 2

    font = pygame.font.Font("Fonts/main_font.ttf", 18)

    # Create a surface for the details box
    details_box = pygame.Surface((box_width, box_height))
    details_box.fill((255, 255, 255))  # White background

    # Load item image from the selected item
    if len(item_images[index]) == 3:
        item_image_path, item_name, item_description, *optional = item_images[index]
    else:
        item_image_path, item_name, item_description, optional = item_images[index]
    item_image = pygame.image.load(item_image_path)
    item_image = pygame.transform.scale(item_image, (95, 95))

    # Draw item image on the details box
    details_box.blit(item_image, (10, 10))

    # Render and draw item name text
    name_text = font.render(item_name, True, (0, 0, 0))
    name_rect = name_text.get_rect(topleft=(110, 20))
    details_box.blit(name_text, name_rect)

    # Render and draw item description text (spanning multiple lines)
    description_lines = textwrap.wrap(item_description, width=32)
    for i, line in enumerate(description_lines):
        line_text = font.render(line, True, (0, 0, 0))
        line_rect = line_text.get_rect(topleft=(110, 60 + i * 20))
        details_box.blit(line_text, line_rect)

    # Check if the item has an optional property
    if optional:
        # Render and draw "Equip" or "Unequip" button
        if len(optional) == 3:
            equip_text = font.render("Unequip" if optional["equipped"] else "Equip", True, (255, 255, 255))
            equip_button_rect = equip_text.get_rect(bottomright=(box_width - 10, box_height - 40))
            pygame.draw.rect(details_box, "#47c0b4", equip_button_rect)
            details_box.blit(equip_text, equip_button_rect)
    else:
        # Render and draw "Use" button
        use_button_text = font.render("Use", True, (255, 255, 255))  # White color for button text
        use_button_rect = use_button_text.get_rect(bottomright=(box_width - 10, box_height - 40))
        pygame.draw.rect(details_box, "#47c0b4", use_button_rect)
        details_box.blit(use_button_text, use_button_rect)

    # Render and draw "Pick Another" button
    pick_another_text = font.render("Pick Another", True, (255, 255, 255))
    pick_another_rect = pick_another_text.get_rect(bottomright=(box_width - 10, box_height - 10))
    pygame.draw.rect(details_box, "#47c0b4", pick_another_rect)
    details_box.blit(pick_another_text, pick_another_rect)

    # Position the details box in the center of the screen
    details_box_rect = details_box.get_rect(center=(width // 2, height // 2))

    # Draw the details box on the screen
    screen.blit(details_box, details_box_rect)

    pygame.display.update()

    # Wait for a key press or click to close the details box
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                relative_mouse_x = mouse_x - details_box_rect.left
                relative_mouse_y = mouse_y - details_box_rect.top
                
                if pygame.Rect.collidepoint(pick_another_rect, relative_mouse_x, relative_mouse_y):
                    # "Pick Another" button clicked
                    waiting_for_input = False

                elif optional and pygame.Rect.collidepoint(equip_button_rect, relative_mouse_x, relative_mouse_y):
                    # "Equip" or "Unequip" button clicked
                    waiting_for_input = False
                    # Toggle the "equipped" property
                    optional["equipped"] = not optional["equipped"]
                    
                    item = combatYelan.getType(item_images[index][3])

                    if optional["equipped"]:
                        combatYelan.equip_artifact(item_images[index])
                    else:
                        combatYelan.unequip_artifact(item_images[index])

                elif not optional and pygame.Rect.collidepoint(use_button_rect, relative_mouse_x, relative_mouse_y):
                    # "Use" button clicked
                    waiting_for_input = False
                    itemUsed = True

                    # Add item to inventory
                    global xlCookingPot
                    global message
                    if item_name not in xlCookingPot:
                        xlCookingPot.append(item_name)
                        message = "You picked " + item_name + "!"
                    else:
                        message = "You already have " + item_name + "!"
                    global inventory_toggle
                    inventory_toggle = False

    pygame.display.update()

def show_character(player):
    global character_toggle

    # Define page dimensions
    page_width, page_height = 400, 480  # Adjust as needed

    # Box dimensions and layout for character page
    box_spacing = 18

    # Font for displaying text
    font = pygame.font.Font("Fonts/main_font.ttf", 16)  # Adjust font size as needed
    
    while character_toggle:
        # Create a surface for the character page
        character_page = pygame.Surface((page_width, page_height))
        character_page.fill("#270023")  # Background color

        # Display character image in the top-left corner
        image = pygame.image.load("Images/yelan_character.png")  # Corrected line
        character_page.blit(image, (box_spacing - 15, box_spacing))  # Display image in the top-left corner

        # Display character stats in the top-right corner
        stats_text = [
            f"HP: {player.max_health}",
            f"Attack: {player.attack}",
            f"Defense: {player.defense}",
            f"Speed: {player.speed}",
            f"Crit Damage: {player.crit_damage}",
            f"Crit Chance: {player.crit_chance}"
        ]
        for i, stat in enumerate(stats_text):
            stat_render = font.render(stat, True, "#47c0b4")
            text_rect = stat_render.get_rect(topleft=(page_width - box_spacing - 120, box_spacing + i * 14))
            character_page.blit(stat_render, text_rect)

        # Display artifacts in two columns
        artifact_x, artifact_y = box_spacing + 40, 135  # Adjusted starting position

        for i, (artifact_type, equipped_artifact) in enumerate(player.equipped.items()):
            if equipped_artifact is not None:
                artifact_box_rect = pygame.Rect(artifact_x + (i % 2) * (page_width // 2) - 40, artifact_y + (i // 2) * 120,
                                            page_width // 2 - 2 * box_spacing, 100)
                pygame.draw.rect(character_page, "#47c0b4", artifact_box_rect, border_radius=10)
                pygame.draw.rect(character_page, "#47c0b4", artifact_box_rect, width=2, border_radius=10)
                # Load artifact image and make it bigger
                artifact_image_surface = pygame.transform.scale(pygame.image.load(equipped_artifact[0]), (100, 100))
                character_page.blit(artifact_image_surface, (artifact_x + (i % 2) * (page_width // 2),
                                                             artifact_y + (i // 2) * 120))

        # Display the character page on the main screen
        screen.blit(character_page, ((screen.get_width() - page_width) // 2, (screen.get_height() - page_height) // 2))
        pygame.display.update()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                character_toggle = not character_toggle
                break
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                character_toggle = False
                pygame.quit()
                quit()

def show_achievements(achievementList):
    global achievements_toggle

    # Box dimensions and layout
    box_width, box_height = 80, 80
    box_outline_thickness = 1
    box_spacing = 18
    num_boxes_per_row = 6
    num_rows = 4

    font = pygame.font.Font(pygame.font.get_default_font(), 18)  # Use a default font for simplicity
    title_text = font.render("Achievements", True, "#270023")
    title_rect = title_text.get_rect(topleft=(10, 10))

    while achievements_toggle == True:
        screen.fill('#47c0b4')
        screen.blit(title_text, title_rect)


        # Draw boxes with item images
        for index, (image_path, item_name, item_description, aquiredProperty) in enumerate(achievementList):
            item_image = pygame.image.load(image_path).convert_alpha()
            item_image = pygame.transform.scale(item_image, (box_width, box_height))
            image_array = pygame.surfarray.array3d(item_image)

            if aquiredProperty.get("aquired", False) is False:
                # Apply Gaussian blur to the image array
                blurred_array = gaussian_filter(image_array, sigma=3)

                # Convert the blurred array back to a surface
                item_image = pygame.surfarray.make_surface(blurred_array)
                item_image.set_alpha(128)
            else:
                # Item acquired, display the image normally
                item_image = pygame.image.load(image_path)
                item_image = pygame.transform.scale(item_image, (box_width, box_height))

            row = index // num_boxes_per_row
            col = index % num_boxes_per_row

            x = col * (box_width + box_spacing) + (width - (num_boxes_per_row * (box_width + box_spacing))) // 2
            y = row * (box_height + box_spacing) + (height - (num_rows * (box_height + box_spacing))) // 2 + 20

            # Draw image on the screen
            screen.blit(item_image, (x, y))

        pygame.display.update()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                achievements_toggle = not achievements_toggle
                break
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                game_loop = False
                pygame.quit()
                quit()

            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if any item is clicked
                for index, (image_path, item_name, item_description, aquiredProperty) in enumerate(achievementList):
                    
                    row = index // num_boxes_per_row
                    col = index % num_boxes_per_row

                    x = col * (box_width + box_spacing) + (width - (num_boxes_per_row * (box_width + box_spacing))) // 2
                    y = row * (box_height + box_spacing) + (height - (num_rows * (box_height + box_spacing))) // 2 + 20

                    # Check if the mouse click is inside the item box
                    if x <= mouse_x <= x + box_width and y <= mouse_y <= y + box_height:
                        # Show item details
                        display_achievement_details(achievementList, index)

def display_achievement_details(achievementList, index):
    # Box dimensions and layout
    box_width, box_height = 435, 180
    box_outline_thickness = 2

    font = pygame.font.Font("Fonts/main_font.ttf", 18)

    # Create a surface for the details box
    details_box = pygame.Surface((box_width, box_height))
    details_box.fill((255, 255, 255))  # White background

    item_image_path, item_name, item_description, aquiredProperty = achievementList[index]
    if aquiredProperty.get("aquired", False) is False:
        item_name = "?????"
        item_description = aquiredProperty.get("message")
        item_image = pygame.image.load(item_image_path).convert_alpha()
        item_image = pygame.transform.scale(item_image, (95, 95))
        image_array = pygame.surfarray.array3d(item_image)

        blurred_array = gaussian_filter(image_array, sigma=3)

        # Convert the blurred array back to a surface
        item_image = pygame.surfarray.make_surface(blurred_array)
        item_image.set_alpha(128)

    else:
        item_image = pygame.image.load(item_image_path)
        item_image = pygame.transform.scale(item_image, (95, 95))

    # Draw item image on the details box
    details_box.blit(item_image, (10, 10))

    wrapped_name_lines = textwrap.wrap(item_name, width=35)

    # Render and draw wrapped item_name text
    for i, line in enumerate(wrapped_name_lines):
        line_text = font.render(line, True, (0, 0, 0))
        line_rect = line_text.get_rect(topleft=(120, 20 + i * 20))
        details_box.blit(line_text, line_rect)

    # Render and draw item description text (spanning multiple lines)
    description_lines = textwrap.wrap(item_description, width=35)
    for i, line in enumerate(description_lines):
        line_text = font.render(line, True, (0, 0, 0))
        line_rect = line_text.get_rect(topleft=(120, 60 + i * 20))
        details_box.blit(line_text, line_rect)

    close_text = font.render("Close", True, (255, 255, 255))
    close_text_rect = close_text.get_rect(bottomright=(box_width - 10, box_height - 10))
    pygame.draw.rect(details_box, "#47c0b4", close_text_rect)
    details_box.blit(close_text, close_text_rect)

    # Position the details box in the center of the screen
    details_box_rect = details_box.get_rect(center=(width // 2, height // 2))

    # Draw the details box on the screen
    screen.blit(details_box, details_box_rect)

    pygame.display.update()

    # Wait for a key press or click to close the details box
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                relative_mouse_x = mouse_x - details_box_rect.left
                relative_mouse_y = mouse_y - details_box_rect.top
                
                if pygame.Rect.collidepoint(close_text_rect, relative_mouse_x, relative_mouse_y):
                    waiting_for_input = False

    pygame.display.update()

def change_scenery():
    pygame.display.update()

def check_recipe(inventory, valid_recipes):
    global achievementList, xlDialogue, shrimpAchievement, stewAchievement, noodleAchievement
    inventory_set = set(inventory)

    for recipe in valid_recipes:
        if set(recipe) == inventory_set:
            if recipe.__contains__("Shrimp meat"):
                shrimpAchievement = True
                xlDialogue = "Dialogues/yelan_xiangling_post-combat_shrimp"
                obtainAchievement(achievementList, "Dew-Dipped Shrimp")
            elif recipe.__contains__("Jueyun Chili"):
                stewAchievement = True
                xlDialogue = "Dialogues/yelan_xiangling_post-combat_stew"
                obtainAchievement(achievementList, "Wanmin Restaurant's Boiled Fish")
            elif recipe.__contains__("Mushroom"):
                noodleAchievement = True
                xlDialogue = "Dialogues/yelan_xiangling_post-combat_noodle"
                obtainAchievement(achievementList, "Heartstring Noodles")
            return True  # If a match is found we exit the loop
    return False

def obtainItem(inventory, itemName):
    for item in inventory:
        if item[1] == itemName:
            item[3]["aquired"] = True
            break

def obtainAchievement(acquiredAchievements, achievementName):
    for achievement in acquiredAchievements:
        if achievement[1] == achievementName:
            achievement[3]["aquired"] = True
            break

pygame.init()

width = 640
height = 480
screen = pygame.display.set_mode((width, height)) # creates display surface
pygame.display.set_caption("Yelan's Oddysey: Inazuma Conundrum")
clock = pygame.time.Clock() # creates clock object

# Menu
main_font = pygame.font.Font('Fonts/main_font.ttf', 50)
line1_surface = main_font.render("Yelan's Odyssey", False, '#308b82')
line2_surface = main_font.render("Inazuma Conundrum", False, '#8E449C')

# Calculate the center coordinates
line1_rect = line1_surface.get_rect(center=(width // 2, 130 - 25))
line2_rect = line2_surface.get_rect(center=(width // 2, 130 + 25))

main_image = pygame.image.load('Fonts/homescreen.png').convert_alpha()
main_image = pygame.transform.scale(main_image, (width, height))

# Buttons
button_group = pygame.sprite.Group()
xl_combat_button_group = pygame.sprite.Group()
combat_button_group = pygame.sprite.Group()
nahida_combat_button_group = pygame.sprite.Group()
xiao_combat_button_group = pygame.sprite.Group()

play_button = Button('Images/Buttons/YelanButton.png', width/2 - 75, 265, 120, 60, "play")
exit_button = Button('Images/Buttons/RaidenButton.png', width/2 - 75, 345, 120, 60, "exit")

button_group.add(play_button)
button_group.add(exit_button)

# Combat Buttons
pick_ingredient_button = Button('Images/Buttons/Ingredient.png', 540, 392, 73, 35, "pick_ingredient")
cook_button = Button('Images/Buttons/Cook.png', 460, 392, 73, 35, "cook")
advice_button = Button('Images/Buttons/Advice.png', 540, 432, 73, 35, "advice")
feed_gouba_button = Button('Images/Buttons/FeedGouba.png', 460, 432, 73, 35, "feed")

xl_combat_button_group.add(pick_ingredient_button)
xl_combat_button_group.add(cook_button)
xl_combat_button_group.add(advice_button)
xl_combat_button_group.add(feed_gouba_button)

attack_button = Button("Images/Buttons/Attack.png", 540, 392, 73, 35, "attack")
special_button = Button("Images/Buttons/Special.png", 460, 392, 73, 35, "special")
talk_button = Button("Images/Buttons/Talk.png", 540, 432, 73, 35, "talk")
flee_button = Button("Images/Buttons/Flee.png", 460, 432, 73, 35, "flee")

combat_button_group.add(attack_button)
combat_button_group.add(special_button)
combat_button_group.add(talk_button)
combat_button_group.add(flee_button)

analyze_button = Button("Images/Buttons/Analyze.png", 540, 392, 73, 35, "analyze")
conclusion_button = Button("Images/Buttons/Conclusion.png", 460, 392, 73, 35, "conclusion")
mind_read_button = Button("Images/Buttons/MindRead.png", 540, 432, 73, 35, "mind_read")
radish_button = Button("Images/Buttons/Radish.png", 460, 432, 73, 35, "radish")

nahida_combat_button_group.add(analyze_button)
nahida_combat_button_group.add(conclusion_button)
nahida_combat_button_group.add(mind_read_button)
nahida_combat_button_group.add(radish_button)

fate_bound_button = Button("Images/Buttons/FateBound.png", 540, 392, 73, 35, "fate_bound")
banish_button = Button("Images/Buttons/Banish.png", 460, 392, 73, 35, "banish")
lament_button = Button("Images/Buttons/Lament.png", 540, 432, 73, 35, "lament")
mercy_button = Button("Images/Buttons/Mercy.png", 460, 432, 73, 35, "mercy")

xiao_combat_button_group.add(fate_bound_button)
xiao_combat_button_group.add(banish_button)
xiao_combat_button_group.add(lament_button)
xiao_combat_button_group.add(mercy_button)

# Player
player = Player(0, 270)
combatYelan = PlayerInCombat(35, 160)

# NPCs
ning_npc = Ning_npc(280, 270, "Images/ning.png", "Dialogue_Images/ning_dialogue.png", "Dialogues/yelan_ning_start", 130, 150)
ganyu_npc = Ganyu_npc(110, 270, "Images/ganyu.png", "Dialogue_Images/ganyu_dialogue.png", "Dialogues/yelan_ganyu_meeting", 130, 150)
xlNpc = Xiangling_npc(340, 245, "Images/xl.png", "Dialogue_Images/xl_dialogue.png", "Dialogues/yelan_xiangling_pre-combat", 100, 150)
laylaNpc = LaylaNpc(110, 230, "Images/layla.png", "Dialogue_Images/layla_dialogue.png", "Dialogues/yelan_layla_meeting", 90, 150)
alhaithamNpc = AlhaithamNpc(110, 230, "Images/alhaitham.png", "Dialogue_Images/alhaitham_dialogue.png", "Dialogues/yelan_alhaitham", 100, 160)
nahidaNpc = NahidaNpc(420, 250, "Images/nahida.png", "Dialogue_Images/nahida_dialogue.png", "Dialogues/yelan_nahida_pre-combat", 130, 150)
amberColleiNpc = AmberColleiNpc(110, 230, "Images/amber_collei.png", "Dialogue_Images/amber_dialogue.png", "Dialogues/amber_collei", 270, 155)
zhongliNpc = ZhongliNpc(380, 230, "Images/zhongli.png", "Dialogue_Images/zhongli_dialogue.png", "Dialogues/yelan_zhongli", 130, 150)
xiaoNpc = XiaoNpc(115, 100, "Images/xiao.png", "Dialogue_Images/xiao_dialogue.png", "Dialogues/yelan_xiao_pre-combat", 130, 150)

# Enemies
combatXl = NpcInCombat(450, 50, "Images/Combat/xlCombat.png", 33, 180, 155)
combatNahida = NpcInCombat(450, 50, "Images/Combat/nahidaCombat.png", 49, 130, 150)
combatSlime = NpcInCombat(320, 320, "Images/Combat/dendro_slime.png", 7, 130, 150)
combatGeoSlime = NpcInCombat(320, 320, "Images/Combat/geo_slime.png", 5, 130, 150)
combatXiao = NpcInCombat(450, 65, "Images/xiao_combo.png", 15, 130, 150)
# Inventory
inventory_toggle = False
inventory_lock = False

# Default inventory when not in combat
artifactInventory = [("Artifacts/NymphDreams/nymph_dreams_flower.png", "Odyssean Flower", "The story must end, and even fresh flowers will wither. But the flower within one's dreams will always remain in full and fragrant bloom.", {"aquired": False, "equipped": False, "type": "flower"}),
                     ("Artifacts/NymphDreams/nymph_dreams_feather.png", "Wicked Mage's Plumule", "This was once a decorative feather in someone's hat. Being dark green, it is quite eye-catching indeed.", {"aquired": False, "equipped": False, "type": "feather"}),
                     ("Artifacts/NymphDreams/nymph_dreams_timepiece.png", "Nymph's Constancy", "A pocket watch that has long stopped working. It seems to have borne witness to many a passing year as its hands spun in vain.", {"aquired": False, "equipped": False, "type": "timepiece"}),
                     ("Artifacts/NymphDreams/nymph_dreams_goblet.png", "Heroes' Tea Party", "A lovely teacup. Perhaps it was once used by people enjoying a leisurely afternoon together.", {"aquired": False, "equipped": False, "type": "goblet"}),
                     ("Artifacts/NymphDreams/nymph_dreams_circlet.png", "Fell Dragon's Monocle", "An exquisitely-made monocle. Ancient anecdotes say that one might be able to see the future through it.", {"aquired": False, "equipped": False, "type": "circlet"})]
specialInventory = [("Inventory/special/qingxin.png", "Qingxin", "A flower that only blooms on the highest mountains. It is said that this flower's petals glow in the dark.", {"aquired": False}),
                    ("Inventory/special/dango.png", "Dango", "A sweet treat made from rice flour. It is said that the more you eat, the more you want. Ei would surely agree.", {"aquired": False}),
                    ("Inventory/special/spider_lily.png", "Spider Lily", "represent remembrance and the impermanence of life. They bloom in adversity, a symbol that beauty can arise from the darkest moments.", {"aquired": False}),
                    ("Inventory/special/osmanthus_wine.png", "Osmanthus Wine", "Osmanthus wine tastes the same as I remember. But where are those who share the memory?", {"aquired": False}),
                    ("Inventory/special/nahida_bell.png", "Rukkhadevata's Bell", "Deck the Halls! *wait, wrong context* A bell that transcends time. It is said that it can open even the best hidden doors.", {"aquired": False})]
defaultInventory = artifactInventory + specialInventory
# Combat inventories and triggers
combatActive = True
itemUsed = False
xlCombatInventory = [("Inventory/xl_combat/ingredients/chili.png", "Jueyun Chili", "A spicy plant native to Liyue. Merely smelling it makes one hot and thirsty."),
                     ("Inventory/xl_combat/ingredients/fish.png", "Fish", "A fish that lives in the sea. A little fishy."),
                     ("Inventory/xl_combat/ingredients/flour.png", "Flour", "The kitchen's fairy dust. The secret to turning your cravings into culinary magic."),
                     ("Inventory/xl_combat/ingredients/fowl.png", "Fowl", "A fresh chunk of fowl. Handled properly, it can make a hearty meal."),
                     ("Inventory/xl_combat/ingredients/ham.png", "Ham", "Smoked leg meat. Even a tiny slice is packed full of flavor."),
                     ("Inventory/xl_combat/ingredients/mushroom.png", "Mushroom", "Sadly a common ingredient, but still a questionable choice."),
                     ("Inventory/xl_combat/ingredients/salt.png", "Salt", "A savory seasoning. A precise but adequate amount will elevate the quality of the cuisine."),
                     ("Inventory/xl_combat/ingredients/shrimp.png", "Shrimp meat", "A whole piece of deep sea shrimp meat, full of nutrients and bursting with delicious flavor."),
                     ("Inventory/xl_combat/ingredients/snapdragon.png", "Snapdragon", "Can be eaten once cooked. As a spice, it can bring wonderful flavor to dishes."),
                     ("Inventory/xl_combat/ingredients/violetgrass.png", "Violetgrass", "A small flower with strong vitality and rich flavors.")]
xlCombatInventoryCopy = copy.deepcopy(xlCombatInventory)
xlCombat = False
xlDialogue = ""
xiaoCombat = False
nahidaCombat = False
nahidaCombatInventory = [("Inventory/nahida_combat/anemo_vision.png", "Anemo Vision", "A vision that allows the user to control the wind. It is said that the wind is the most gentle of all elements."),
                         ("Inventory/nahida_combat/geo_vision.png", "Geo Vision", "A vision that allows the user to control the earth. It is said that the earth is the most stable (unlike this code) of all elements."),
                         ("Inventory/nahida_combat/electro_vision.png", "Electro Vision", "A vision that allows the user to control lightning. It is said that lightning is the most powerful of all elements."),
                         ("Inventory/nahida_combat/paper1.png", "Inazuma newsletter", "A newsletter from Inazuma about a food party that the Electro Archon is hosting. With food cooked by the Raiden Shogun herself, it is said that the food is to die for."),
                         ("Inventory/nahida_combat/paper2.png", "Mondstadt newspaper", "A newspaper from Mondstadt about a new festival that is being held in the city. It is said that the festival is to celebrate the Windblume festival, with music from the famous drunkard bard."),
                         ("Inventory/nahida_combat/paper3.png", "Liyue newspaper", "A newspaper from Liyue about a new festival that is being held in the city. It is said that the festival is to celebrate the 1000th anniversary of the city, with the finest wine."),
                         ("Inventory/nahida_combat/inazumapic1.png", "Inazuma storm", "A picture of the storm that is surrounding Inazuma. Rumors say that the storm started not long after the preparations for the festival started."),
                         ("Inventory/nahida_combat/inazumapic2.png", "Corruption Pustule", "A picture of the Corruption Pustule behind Inazuma, cursing tree roots along Inazuma, Liyue and even Sumeru."),
                         ("Inventory/nahida_combat/inazumapic3.png", "Sacred Sakura Tree", "A picture of the Sacred Sakura Tree, where Yae Miko resides. She is Inazuma's head shrine maiden, Raiden's closest friend a good friend of the Geo Archon"),]
xlCookingPot = []
valid_recipes = [
        ["Flour", "Fowl", "Mushroom", "Ham"],
        ["Fish", "Jueyun Chili", "Salt", "Violetgrass"],
        ["Shrimp meat", "Flour", "Salt", "Snapdragon"]]
valid_conclusions = [["Electro Vision", "Inazuma newsletter", "Inazuma storm"]]
turn = "player"

xiaoCombatInventory = []

# Character
character_toggle = False

# Achievements
achievements_toggle = False
achievement_lock = False

# If they become true, the achievement will be shown clearly
ningAchievement = False
ganyuAchievement = False
xlAchievement = False
shrimpAchievement = False
noodleAchievement = False
stewAchievement = False
foodCompleteAchievement = False
goubaAchievement = False
laylaAchievement = False
alhaithamAchievement = False
yelanLoveAchievement = False
nahidaAchievement = False
radishAchievement = False
amberColleiAchievement = False
zhongliAchievement = False
xiaoAchievement = False
completionistAchievement = False

achievementList = [ ("Achievements/yelan_achievement.png", "Yelan", "Just Yelan", {"aquired": True, "message": "Still Yelan"}),
                    ("Achievements/ning_achievement.png", "Not again", "Have a mission ruin your holiday…again!", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/ganyu_achievement.png", "Let it snow", "Be blessed by the Qilin’s Celestial Shower", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/xl_achievement.png", "Adeptus' Temptation", "Aquire the Legendary Dango, a delightful treat, fit for an archon.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/dew-dipped_shrimp_achievement.png", "Dew-Dipped Shrimp", "The look is sightly, the scent of distant tea, and the taste both tender and springy.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/heartstring_noodles_achievement.png", "Heartstring Noodles", "A dish that is as soft as a song, and as tender as a poem, made with love for Shenhe.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/xiangling_special_achievement.png", "Wanmin Restaurant's Boiled Fish", "Anyone who tastes it will gain a pure appreciation for gourmet food amid the hearty and addictive blend of flavors.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/food_complete_achievement.png", "Never too much food?", "You've had so much food, but Ganyu still offers you a hearty meal of flowers.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/gouba_achievement.png", "Gouba? Gouba!", "Today is a Gouba holiday. Celebrate by feeding Gouba! May Gouba's happiness never end!", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/amber_collei_achievement.png", "A bridge between Nations", "Is this foreshadowing?", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/zhongli_achievement.png", "Osmanthus wine tastes the same as I remember…", "…But where are those who share the memory?", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/xiao_achievement.png", "Dispel the Evil", "Befriend the *small* strong Yaksha", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/layla_achievement.png", "Half-awake, half-asleep", "Meet Layla..wait, was that actually her?", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/yelan_love_achievement.png", "Serendipitous Symphony", "All space and time are practically infinite, and yet right here, right now, we find ourselves together.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/alhaitham_achievement.png", "A dance with imperfection", "That's the nature of destiny — it creates a miracle but convinces you of an accident.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/nahida_achievement.png", "Swinging in the realm of the Divine", "Meet the Dendro Archon and see deep into their minds", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/radish_achievement.png", "Way too many radishes", "Haven't you had enough radishes? They even went out of stock, so you got a wild Kazuha instead.", {"aquired": False, "message": "The stars are not aligned."}),
                    ("Achievements/completionist_achievement.png", "Pure Completion", "You went above and beyond and optained 112%. Silksong is still TBD, but I hope you enjoyed this journey", {"aquired": False, "message": "The stars are not aligned."})]

# Special toggles
zhongliVisible = False

#Game loop
game_loop = True
fullscreen = False
talking = False

current_scene = YelanNingScene(player, screen, ning_npc)
current_inventory = defaultInventory

while game_loop:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            game_loop = False
            pygame.quit()
            quit()
        if keys[pygame.K_F4] and fullscreen == False: # F4 key
            pygame.display.toggle_fullscreen()
            fullscreen = True
        elif keys[pygame.K_F4] and fullscreen == True:
            # make it windowed again
            pygame.display.set_mode((width, height))
            fullscreen = False
        if button_group.sprites()[0].start_game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i and inventory_lock == False:
                    inventory_toggle = not inventory_toggle
                elif event.key == pygame.K_c:
                    character_toggle = not character_toggle
                elif event.key == pygame.K_e and achievement_lock == False:
                    achievements_toggle = not achievements_toggle
                if current_scene.get_npc() != None:
                    if pygame.sprite.collide_rect(player, current_scene.get_npc()) and event.key == pygame.K_f:
                        talking = not talking
                    elif pygame.sprite.collide_rect(player, current_scene.get_npc()) == False:
                        talking = False

    if button_group.sprites()[0].start_game:
        
        # Game functions
        if inventory_toggle == True:
            show_inventory(current_inventory)
        if character_toggle == True:
            show_character(combatYelan)
        if achievements_toggle == True:
             # If all food achievements are True, foodCompleteAchievement will be True
            foodList = [shrimpAchievement, noodleAchievement, stewAchievement]
            if foodList.count(True) == len(foodList):
                foodCompleteAchievement = True
                obtainAchievement(achievementList, "Never too much food?")
            
            # If all achievements are True, completionistAchievement will be True
            completionistList = [ningAchievement, ganyuAchievement, xlAchievement, goubaAchievement, laylaAchievement, alhaithamAchievement, nahidaAchievement, amberColleiAchievement, zhongliAchievement, xiaoAchievement, yelanLoveAchievement, foodCompleteAchievement, goubaAchievement, radishAchievement]
            if completionistList.count(True) == len(completionistList):
                completionistAchievement = True
                obtainAchievement(achievementList, "Pure Completion")
                
            show_achievements(achievementList)

        current_scene.update()

    else:
        screen.blit(main_image, (0, 0))
        screen.blit(line1_surface, line1_rect)
        screen.blit(line2_surface, line2_rect)

        # display buttons
        display_offset = 0
        for button in button_group:
            screen.blit(button.image, (width/2 - button.width/2, 265 + display_offset))
            display_offset += 80

        button_group.update()

    pygame.display.update() # updates the display surface
    clock.tick(60) # frame ceiling
    