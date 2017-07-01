from pyganim import *


class PygAnimation(PygAnimation):
    def blit(self, destSurface, dest=(0, 0), area=None):
        # Draws the appropriate frame of the animation to the destination Surface
        # at the specified position.
        #
        # NOTE: If the visibility attribute is False, then nothing will be drawn.
        #
        # @param destSurface
        #     The Surface object to draw the frame
        # @param dest
        #     The position to draw the frame. This is passed to Pygame's Surface's
        #     blit() function, so it can be either a (top, left) tuple or a Rect
        #     object.
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        frameNum = findStartTime(self._startTimes, self.elapsed)
        destSurface.blit(self.getFrame(frameNum), dest, area)