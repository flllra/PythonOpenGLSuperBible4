#!/usr/bin/env python
# points.py
# Demonstates OpenGL Primitive GL_POINTS
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: points.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key

xRot = 0.0
yRot = 0.0

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Setup the rendering state
        glClearColor(0, 0, 0, 1)
        
        # Set drawing color to green
        glColor3f(0, 1, 0)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Save matrix state and do the rotation
        glPushMatrix()
        glRotatef(xRot, 1, 0, 0)
        glRotatef(yRot, 0, 1, 0)
        
        # Get supported point size range and step size
        sizes = (GLfloat * 2)()
        step = GLfloat()
        
        glGetFloatv(GL_POINT_SIZE_RANGE, sizes)
        glGetFloatv(GL_POINT_SIZE_GRANULARITY, byref(step))
        
        # Set initial point size
        curSize = sizes[0]
        
        z = -50.0
        angle = 0.0
        while angle < (2.0 * 3.14159) * 3.0:
            x = 50.0 * math.sin(angle)
            y = 50.0 * math.cos(angle)
            
            # Specifiy the point size before the primitive is specified
            glPointSize(curSize)
            
            # Draw the point
            glBegin(GL_POINTS)
            glVertex3f(x, y, z)
            glEnd()
            
            z += 0.5
            angle += 0.1
            curSize += step.value
        
        # Restore transformations
        glPopMatrix()
        
        # Flush drawing commands
        # pyglet does this automatically when using pyglet.app.run()
        # otherwise, you can use flip() http://pyglet.org/doc/programming_guide/windows_and_opengl_contexts.html

    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        nRange = 100.0
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        if w <= h:
            glOrtho (-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
        else:
            glOrtho (-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_key_press(self, symbol, modifier):
        global xRot, yRot
        if symbol == key.UP:
            xRot -= 5.0
        elif symbol == key.DOWN:
            xRot += 5.0
        elif symbol == key.LEFT:
            yRot -= 5.0
        elif symbol == key.RIGHT:
            yRot += 5.0
        
        if xRot > 356.0:
            xRot = 0.0
        elif xRot < -1.0:
            xRot = 355.0
        if yRot > 356.0:
            yRot = 0.0
        if yRot < -1.0:
            yRot = 355.0
            
    

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(caption='Points Example', resizable=True)
    pyglet.app.run()
