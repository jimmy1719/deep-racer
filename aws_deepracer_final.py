#Tuesday Week 3, add more speed related rewards
import math

def reward_function(params):
    ###############################################################################
    '''
    Example of using waypoints and heading to make the car point in the right direction
    '''

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed=params['speed']

    # Initialize the reward with typical value
    reward_t = 1.0
    
    #Create degList
    wpList=[]
    for x in range(len(waypoints)):
        wpList.append(waypoints[x])
    print('wpList:',wpList)
    degList=[]
    degListDiff=[]
    for x in range(len(wpList)):
        if x==len(wpList)-1:
            p1=wpList[0]
            p0=wpList[x]
            nextDirection=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
            nextDirection=math.degrees(nextDirection)
            # if nextDirection < 0:
            #     degList.append(nextDirection+360)
            # else:
            degList.append(nextDirection)
        else:
            p1=wpList[x+1]
            p0=wpList[x]
            nextDirection=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
            nextDirection=math.degrees(nextDirection)
            # if nextDirection > 180:
            #     degList.append(nextDirection-360)
            # else:
            degList.append(nextDirection)
    print('degList',degList)
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
                      
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    
    #Determine next turn degrees, pull from degList
    for x in range(len(wpList)):
        if wpList[x]==waypoints[closest_waypoints[1]]:
            if x==len(wpList)-2:
                nextDir=degList[len(wpList)-1]
                skipAhead=degList[0]
            elif x==len(wpList)-1:
                nextDir=degList[0]
                skipAhead=degList[1]
            else:
                nextDir=degList[x]
                skipAhead=degList[x+1]
    
    headingThreshold=5
    headingCenter=(nextDir-track_direction)/2
    
    skipAheadThreshold=4
    skipAheadCenter=(headingCenter-skipAhead)/2
    
    #Curve Prep
    if (heading<headingCenter+headingThreshold) and (heading>headingCenter-headingThreshold):
        if (heading<skipAheadCenter+skipAheadThreshold) and (heading>skipAheadCenter-skipAheadThreshold):
            reward_t=1.0
        else:
            reward_t=0.9
    
    #Track Width Rewards
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_3 = 0.35 * track_width
    if distance_from_center <= marker_1:
        reward_t *= 1.0
    elif distance_from_center <= marker_2:
        reward_t *= 0.95
    elif distance_from_center <= marker_3:
        reward_t = 0.7
    else:
        reward_t = 1e-3  # likely crashed/ close to off track
            
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 25
    if direction_diff > DIRECTION_THRESHOLD:
    # Give higher reward if the car is closer to center line and vice versa
        reward_t = 1e-3
    
    # Define SPEED rewards!
    reward_s = 1.0
    if speed > 3.0:
        reward_s *= 1.0
    elif speed > 2.75:
        reward_s *= 0.95
    elif speed > 2.5:
        reward_s *= 0.85
    elif speed > 2.0:
        reward_s *= 0.7
    elif speed > 1.8:
        reward_s *= 0.6
    else:
        reward_s=1e-3
    
    # Weighting Function
    accuracy_weight=0.4
    reward=accuracy_weight*reward_t+(1-accuracy_weight)*reward_s        
    
    return float(reward)