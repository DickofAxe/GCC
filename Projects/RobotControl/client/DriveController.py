import paho.mqtt.client as mqtt
import pygame, sys, os
import agent

pygame.init()
bigFont = pygame.font.SysFont("apple casual", 48)
frameclock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600))

client = mqtt.Client("DriveController")


def onConnect(client, data, rc):
    if rc == 0:
        print("Connected")
        agent.init(client, "DriveAgent.py")
    else:
        print("Connection returned error result: " + str(rc))
        os._exit(rc)

def onMessage(client, data, msg):
    global exit

    if agent.process(msg):
        if agent.returncode("DriveAgent") != None:
            exit = True
    else:
        print("Wrong topic '" + msg.topic + "'")


client.on_connect = onConnect
client.on_message = onMessage

print("DriveController: Starting...")
client.connect("172.24.1.185", 1883, 60)


rects = {
    "UP": pygame.Rect(200, 0, 200, 200),
    "DOWN": pygame.Rect(200, 400, 200, 200),
    "LEFT": pygame.Rect(0, 200, 200, 200),
    "RIGHT": pygame.Rect(400, 200, 200, 200),
    "SPEED": pygame.Rect(200, 200, 200, 200),
}



straight = True

danceTimer = 0
speed = 50


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                speed = speed - 1
            if event.button == 4:
                speed = speed + 1
            speed = speed % 100
            print("New speed: " + str(speed))

    keys = pygame.key.get_pressed()

    client.loop()
    screen.fill((0, 0, 0))

    if keys[pygame.K_w]:
        client.publish("drive", "forward>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
    elif keys[pygame.K_s]:
        client.publish("drive", "back>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_a]:
        client.publish("drive", "crabLeft>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
    elif keys[pygame.K_d]:
        client.publish("drive", "crabRight>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_q]:
        client.publish("drive", "pivotLeft>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
    elif keys[pygame.K_e]:
        client.publish("drive", "pivotRight>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_x]:
        client.publish("drive", "align")
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_c]:
        client.publish("drive", "align")
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_v]:
        client.publish("drive", "slant")
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_SPACE]:
        if danceTimer >= 10:
            client.publish("drive", "slant")
            pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
            pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
            pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
            pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
        elif danceTimer <= 10:
            client.publish("drive", "align")
    elif keys[pygame.K_UP]:
        client.publish("drive", "motors>" + str(speed))
    elif keys[pygame.K_DOWN]:
        client.publish("drive", "motors>" + str(-speed))
    elif keys[pygame.K_1]:
        speed = 50
        print("New speed: " + str(speed))
    elif keys[pygame.K_2]:
        speed = 75
        print("New speed: " + str(speed))
    elif keys[pygame.K_3]:
        speed = 100
        print("New speed: " + str(speed))
    elif keys[pygame.K_4]:
        speed = 150
        print("New speed: " + str(speed))
    elif keys[pygame.K_5]:
        speed = 200
        print("New speed: " + str(speed))
    elif keys[pygame.K_5]:
        speed = 300
        print("New speed: " + str(speed))
    else:
        client.publish("drive", "stop")


    danceTimer += 1
    danceTimer = danceTimer % 20

    value = speed + 155
    if (value > 255):
        value = 255
    elif value < 1:
        value = 0


    pygame.draw.rect(screen, (value, value, value), rects["SPEED"])

    text = bigFont.render("Speed: " + str(speed), 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 0, 0, 0))

    pygame.display.flip()
    frameclock.tick(30)