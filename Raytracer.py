import numpy as np
import matplotlib.pyplot as plt
import math

from vector_class import Vector

# Functions=============================================================================================================================

def SaveImage(image, width, height):
    imageName = input("Your image name:")

    path = 'C:/Users/tnoye/Documents/Personnel/Programmation/Python/Raytracing/RaytracerFromScratch/Results/'
    fileName = path + imageName + '(%dX%d).png' % (width, height)
    plt.imsave(fileName, image)
    print("Your image was successfully saved! \nPath: " + path)

def sphereIntersect(center:Vector, radius, ray_origin:Vector, ray_direction:Vector):
    b = ray_direction.dotProduct(ray_origin - center) * 2
    c = Vector.length(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c

    if delta > 0:
        t1 = (-b + math.sqrt(delta)) / 2
        t2 = (-b - math.sqrt(delta)) / 2

        if t1 > 0 and t2 > 0:
            intersection = ray_origin + ray_direction * min(t1, t2)
            if intersection is None: print(type(t1), type(t2))
            normal = Vector.normalize(intersection - center)
            return min(t1, t2), normal
    return None, None

def triangleIntersect(point1, point2, point3, ray_origin, ray_direction):
    E1 = point2 - point1
    E2 = point3 - point1
    Pvec = 0


def planeIntersect(distance, normal, ray_origin, ray_direction):
    dotDir = normal.dotProduct(ray_direction)
    dot = normal.dotProduct(ray_origin)
    dist = (dot + distance) / dotDir

    if dotDir!=0 and dist<0:
        return -dist, normal.normalize()
    else: return None, None


def nearestIntersectedObject(objects, ray_origin, ray_direction):
    distances = []
    normals = []
    for obj in objects:
        if obj['type'] == 'sphere':
            distance, normal = sphereIntersect(obj['center'], obj['radius'], ray_origin, ray_direction)
            distances.append(distance)
            normals.append(normal)

        elif obj['type'] == 'plane':
            distance, normal = planeIntersect(obj['distance'], obj['normal'], ray_origin, ray_direction)
            distances.append(distance)
            normals.append(normal)


    nearestObject = None
    minDistance = np.inf
    normalToSurface = Vector(0, 0, 0)
    for i, distance in enumerate(distances):
        if distance and distance < minDistance:

            minDistance = distance
            nearestObject = objects[i]
            normalToSurface = normals[i]

    return nearestObject, minDistance, normalToSurface

def reflectedRay(vector, axis):
    return vector - axis * Vector.dotProduct(vector, axis) * 2


# Main Script=============================================================================================================================

width, height = 300, 200
maxDepth = 3

ratio = float(width) / height
screen = (-1, 1/ratio, 1, -1/ratio)

camera = 0
cameraPos = Vector(0, 0, 1)
cameraDir = Vector(0, 0, 0)
volumetric = True
volumetricMaxDistance = 10
volumetricChecks = 10
volumetricDensity = 1.0
volumetricColor = Vector(1, 1, 1)

FOV = 1

objects = [
    { 'type': 'sphere', 'center': Vector(-0.2, 0, -1), 'radius': 0.7, 'ambient': Vector(0.1, 0, 0), 'diffuse': Vector(0.7, 0, 0), 'specular': Vector(1, 1, 1), 'shininess': 100, 'reflection': 0.5 },
    { 'type': 'sphere', 'center': Vector(0.1, -0.3, 0), 'radius': 0.1, 'ambient': Vector(0.1, 0, 0.1), 'diffuse': Vector(0.7, 0, 0.7), 'specular': Vector(1, 1, 1), 'shininess': 100, 'reflection': 0.1 },
    { 'type': 'sphere', 'center': Vector(-0.3, 0, 0), 'radius': 0.15, 'ambient': Vector(0, 0.1, 0), 'diffuse': Vector(0, 0.6, 0), 'specular': Vector(1, 1, 1), 'shininess': 100, 'reflection': 0.3 },
    #{ 'type': 'sphere', 'center': Vector(0, -9000, 0), 'radius': 9000-0.7, 'ambient': Vector(0.1, 0.1, 0.1), 'diffuse': Vector(0.6, 0.6, 0.6), 'specular': Vector(1, 1, 1), 'shininess': 100, 'reflection': 0.5 },
    { 'type': 'plane', 'distance': 0.6, 'normal': Vector(0, 1, 0), 'ambient': Vector(0.1, 0.1, 0.1), 'diffuse': Vector(0.6, 0.6, 0.6), 'specular': Vector(1, 1, 1), 'shininess': 100, 'reflection': 0.3 }
]

light = { 'position': Vector(5, 5, 5), 'ambient': Vector(1, 1, 1), 'diffuse': Vector(1, 1, 1), 'specular': Vector(1, 1, 1) }

skyDiffuse = Vector(0.41, 0.72, 1)

image = np.zeros((height, width, 3))

# Main loop
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # Creates vectors
        pixel = Vector(x, y, -FOV) + cameraPos

        # DOP: Depth Of Field. Default value of DOPStrength is 0.
        #DOFstrength = 10
        #DOFtargetDist = 10
        #disturbance = Vector(DOPstrength, DOPstrength, 0)


        origin = cameraPos
        direction = Vector.normalize(pixel - origin)
        direction = Vector.normalize(direction + cameraDir)
        #DOFdirection  = direction * DOFstrength
        #DOFdirection.z = direction.z
        #direction = Vector.normalize((direction * DOFtargetDist) - (DOFdirection.normalize() * 0.5))


        #color = Vector(0.2, 0.64, 1)
        color = Vector(0, 0, 0)
        reflection = 1

        for k in range(maxDepth):
            nearestObject, minDistance, normalToSurface = nearestIntersectedObject(objects, origin, direction)
            if nearestObject is None:
                color += skyDiffuse * reflection
                break

            intersection = origin + direction * minDistance
            #normalToSurface = Vector.normalize(intersection - nearestObject['center'])
            
            shiftedPoint = intersection + normalToSurface * 1e-5
            intersectionToLight = Vector.normalize(light['position'] - shiftedPoint)

            _, minDistance, _a = nearestIntersectedObject(objects, shiftedPoint, intersectionToLight)
            intersectionToLightDistance = Vector.length(light['position'] - intersection)
            isShadowed = minDistance < intersectionToLightDistance

            #if isShadowed:
                #color += nearestObject['diffuse'] * skyDiffuse * reflection
                #break

            illumination = Vector(0, 0, 0)

            # Ambient
            illumination += nearestObject['ambient'] * light['ambient']

            # Diffuse
            illumination += nearestObject['diffuse'] * light['diffuse'] * Vector.dotProduct(intersectionToLight, normalToSurface)

            # Specular
            intersectionToCamera = Vector.normalize(cameraPos - intersection)
            H = Vector.normalize(intersectionToLight + intersectionToCamera)
            illumination += nearestObject['specular'] * light['specular'] * Vector.dotProduct(normalToSurface, H) ** (nearestObject['shininess'] / 4)

            if isShadowed:
                illumination = illumination/2 #* skyDiffuse --Version bleue

            # Volumetrics
            if False: #volumetric:
                distance = min(minDistance, volumetricMaxDistance) if minDistance!=np.inf else volumetricMaxDistance
                totalSteps = int(distance * volumetricChecks)

                for t in np.linspace(distance - 0.01, 0, totalSteps):
                    dustCoord = origin + direction * direction
                    dustColor = volumetricColor

                    if volumetric and volumetricDensity != 0:
                        dustShadowMultiplier = Vector(1, 1, 1)
                        
                        _, minDistance = nearestIntersectedObject(objects, dustCoord, Vector.normalize(light['position'] - dustCoord))
                        if minDistance < intersectionToLightDistance:
                            dustShadowMultiplier = Vector(0, 0, 0)

                        dustColor *= dustShadowMultiplier
                        amount = volumetricDensity / 100 / volumetricChecks
                        color += (dustColor - color) * amount

            # Reflection
            color += illumination * reflection
            reflection *= nearestObject['reflection']

            origin = shiftedPoint
            direction = direction - normalToSurface * 2 * Vector.dotProduct(direction, normalToSurface)   #vector, axis

        # post-process
        """
        exposure = 0.66
        color.x = -(1.0 - math.exp(color.x * exposure))# + 1
        color.y = -(1.0 - math.exp(color.y * exposure))# + 1
        color.z = -(1.0 - math.exp(color.z * exposure))# + 1
        """

        gamma = 1
        #color = color ** gamma

        #print(color)
        color.clip(0, 1)
        image[i, j] = [color.x, color.y, color.z]
    print("%d/%d" % (i+1, height))


SaveImage(image, width, height)
