import pygame
from player import Player

class PlayerInCombat(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('Images/Combat/yelan_piglet.png').convert_alpha() # insert combat image here
        self.image = pygame.transform.scale(self.image, (185, 230))
        self.rect = self.image.get_rect()
        self.max_health = 100
        self.remaining_health = self.max_health
        self.crit_damage = 300
        self.crit_chance = 100
        self.attack = 10
        self.defense = 10
        self.speed = 170
        self.rect.x = x
        self.rect.y = y
        # stats list
        self.stats = [self.max_health, self.remaining_health, self.crit_damage, self.crit_chance, self.attack, self.defense, self.speed]
        self.artifactInventory = [("Artifacts/NymphDreams/nymph_dreams_flower.png", "Odyssean Flower", "The story must end, and even fresh flowers will wither. But the flower within one's dreams will always remain in full and fragrant bloom.", {"aquired": False, "equipped": False, "type": "flower"}),
                     ("Artifacts/NymphDreams/nymph_dreams_feather.png", "Wicked Mage's Plumule", "This was once a decorative feather in someone's hat. Being dark green, it is quite eye-catching indeed.", {"aquired": False, "equipped": False, "type": "feather"}),
                     ("Artifacts/NymphDreams/nymph_dreams_timepiece.png", "Nymph's Constancy", "A pocket watch that has long stopped working. It seems to have borne witness to many a passing year as its hands spun in vain.", {"aquired": False, "equipped": False, "type": "timepiece"}),
                     ("Artifacts/NymphDreams/nymph_dreams_goblet.png", "Heroes' Tea Party", "A lovely teacup. Perhaps it was once used by people enjoying a leisurely afternoon together.", {"aquired": False, "equipped": False, "type": "goblet"}),
                     ("Artifacts/NymphDreams/nymph_dreams_circlet.png", "Fell Dragon's Monocle", "An exquisitely-made monocle. Ancient anecdotes say that one might be able to see the future through it.", {"aquired": False, "equipped": False, "type": "circlet"})]
        # here we save the currently equipped artifacts. i think we can save self.artifactInventory[index]
        self.equipped = {"flower": None, "feather": None, "timepiece": None, "goblet": None, "circlet": None}

    def lock_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 0
        if keys[pygame.K_s]:
            self.rect.y += 0
        if keys[pygame.K_a]:
            self.rect.x -= 0
        if keys[pygame.K_d]:
            self.rect.x += 0

    # Gets artifact type
    def getType(self, item):
        if "type" in item:
            return item["type"]
        else:
            return None
    
    # Checks if artifact is equipped
    def isEquipped(self, item):
        if "equipped" in item[3]:
            return item[3]["equipped"]
        else:
            return None

    # Searches for a equipped artifact of a certain type
    # If there is no artifact equipped, it returns None
    # Else, it returns the artifact
    def searchArtifact(self, searchedType):
        for artifact in self.artifactInventory:
            if self.getType(artifact) == searchedType and self.isEquipped(artifact) == True:
                return artifact
        return None

    # Equips an artifact
    # If one is already equipped, it unequips it and equips the new one
    # It also updates the equipped list
    # And sets the equipped properties of the artifacts
    def equip_artifact(self, item):
        for i, artifact in enumerate(self.artifactInventory):
            if artifact[1] == item[1]:  # Assuming the name is unique
                artifact_type = artifact[3]['type']
                
                # Check if there's already an artifact equipped in the same category
                if self.equipped[artifact_type] is not None:
                    previous_equipped_name = self.equipped[artifact_type]
                    
                    # Unequip the previously equipped artifact
                    for j, prev_artifact in enumerate(self.artifactInventory):
                        if prev_artifact[1] == previous_equipped_name:
                            self.artifactInventory[j][3]['equipped'] = False
                            break
                
                # Update the 'equipped' status in the inventory for the new artifact
                self.artifactInventory[i][3]['equipped'] = True
                
                # Update the 'equipped' dictionary
                self.equipped[artifact_type] = item

                break

    # Unequips an artifact
    def unequip_artifact(self, item):
        if self.equipped[item[3]["type"]] is not None:
            equipped_name = self.equipped[item[3]["type"]]
            
            # Update the 'equipped' status in the inventory for the unequipped artifact
            for i, artifact in enumerate(self.artifactInventory):
                if artifact[1] == equipped_name:
                    self.artifactInventory[i][3]['equipped'] = False
                    break
            
            # Update the 'equipped' dictionary to reflect the unequipping
            self.equipped[item[3]["type"]] = None

    def take_damage(self, damage):
        self.remaining_health -= damage

    def update(self):
        self.lock_movement()
