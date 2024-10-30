import math

import adafruit_bno08x
import adafruit_bno08x.i2c
import board
import busio
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class BNO085Visualization:

    def __init__(self):
        self.bno085 = adafruit_bno08x.i2c.BNO08X_I2C(busio.I2C())
        self.bno085.initialize()
        self.bno085.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
        self.bno085.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
        self.bno085.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
        self.bno085.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)
        self.bno085.begin_calibration()

    def quaternion_to_euler(self, q):
        w, x, y, z = q

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)

        quaternion = self.bno085.quaternion
        roll, pitch, yaw = self.quaternion_to_euler(quaternion)

        glRotatef(math.degrees(roll), 1, 0, 0)
        glRotatef(math.degrees(pitch), 0, 1, 0)
        glRotatef(math.degrees(yaw), 0, 0, 1)

        glutSolidTeapot(1.0)
        glutSwapBuffers()

    def update(self, _):
        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0)

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(500, 500)
        glutCreateWindow("BNO085 Visualization")

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        light_pos = [10.0, 10.0, 10.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glViewport(0, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1, 1, 50)
        glMatrixMode(GL_MODELVIEW)

        glutDisplayFunc(self.display)
        glutTimerFunc(0, self.update, 0)
        glutMainLoop()


def main():
    bno085_visualization = BNO085Visualization()
    bno085_visualization.run()


if __name__ == "__main__":
    main()
