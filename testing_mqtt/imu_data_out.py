# отсюда: https://github.com/thecountoftuscany/PyTeapot-Quaternion-Euler-cube-rotation
import math

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.time import wait

imu_filename = 'imu_data.txt'


# import serial
# ser = serial.Serial('/dev/ttyUSB0', 38400)
# ser = serial.Serial('COM7', 115200)

# import socket
# UDP_IP = "0.0.0.0"
# UDP_PORT = 5005
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
# sock.bind((UDP_IP, UDP_PORT))


def main():
    f = open(imu_filename, "r")
    f.seek(0, 2)  # jump to end
    endfile = f.tell()  # save end
    f.seek(0)

    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((640, 480), video_flags)
    print(screen)
    pygame.display.set_caption("IMU visualization")
    resizewin(640, 480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()

    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        # строка из файла:
        # INFO:root:parsed data: ['0.734314', '0.677612', '0.039429', '-0.008240']

        line = f.readline().replace('\n', '')
        if line == '' and f.tell() == endfile:  # повтор файла
            f.seek(0)
            print('\n' * 50)
            wait(2000)

        if 'INFO:root:parsed data:' in line:
            qq = ((line.split('[')[1]).split(']')[0]).replace("'", '').split(',')  # вырезать [текст в скобках], удалить кавычки и разделить по запятой
            print(qq)

            ww = float(qq[0])
            xx = float(qq[1])
            yy = float(qq[2])
            zz = float(qq[3])

            draw(ww, xx, yy, zz)
            pygame.display.flip()
            frames += 1
            wait(15)  # milliseconds

    print("fps: %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks)))
    f.close()
    # ser.close()


def resizewin(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


# def read_data(line):
# if (useSerial):
#   ser.reset_input_buffer()
#   cleanSerialBegin()
#   line = ser.readline().decode('UTF-8').replace('\n', '')
#   line = 'w0.09wa-0.12ab-0.09bc0.98c'
#   print(line)
# else:
#     Waiting for data from udp port 5005
#     data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
#     line = data.decode('UTF-8').replace('\n', '')
#     print(line)


def draw(w, nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    # drawText((-2.6, 1.8, 2), "PyTeapot", 18)
    # drawText((-2.6, 1.6, 2), "Module to visualize quaternion or Euler angles data", 16)
    drawText((-2.6, -2, 2), "Press Escape to exit.", 16)

    [yaw, pitch, roll] = quat_to_ypr([w, nx, ny, nz])
    drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" % (yaw, pitch, roll), 16)
    glRotatef(2 * math.acos(w) * 180.00 / math.pi, -1 * nx, nz, ny)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()


def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def quat_to_ypr(q):
    yaw = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.sin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw *= 180.0 / math.pi
    yaw -= -0.13  # Declination at Chandrapur, Maharashtra is - 0 degress 13 min
    roll *= 180.0 / math.pi
    return [yaw, pitch, roll]


if __name__ == '__main__':
    main()
