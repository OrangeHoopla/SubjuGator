import txros
from twisted.internet import defer
from ros_alarms import TxAlarmListener, TxAlarmBroadcaster
from mil_misc_tools import text_effects

# Import missions here
import square
import buoy
import align_path_marker
import torpedos
import bin_dropper
import surface
import start_gate

fprint = text_effects.FprintFactory(title="AUTO_MISSION").fprint


@txros.util.cancellableInlineCallbacks
def do_mission_square(sub):
    fprint("RUNNING SQUARE MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield square.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("SQUARE MISSION COMPLETE", msg_color="green")



def do_mission_buoy(sub):
    fprint("RUNNING BUOY MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield buoy.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("BUOY MISSION COMPLETE", msg_color="green")



def do_mission_align(sub):
    fprint("RUNNING ALIGN PATH MARKER MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield align_path_marker.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("ALIGN PATH MARKER MISSION COMPLETE", msg_color="green")



def do_mission_start_gate(sub):
    fprint("RUNNING START GATE MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield start_gate.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("START GATE MISSION COMPLETE", msg_color="green")



def do_mission_torpedos(sub):
    fprint("RUNNING TORPEDO MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield torpedos.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("TORPEDO MISSION COMPLETE", msg_color="green")



def do_mission_bin_dropper(sub):
    fprint("RUNNING SQUARE MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield bin_dropper.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("SQUARE MISSION COMPLETE", msg_color="green")



def do_mission_surface(sub):
    fprint("RUNNING SQUARE MISSION", msg_color="blue")

    # Chain 1 missions
    try:
        yield surface.run(sub)
    except Exception as e:
        fprint("Error in Chain 1 missions!", msg_color="red")
        print e

    # Create a mission kill alarm and kill in the final area
    ab = yield TxAlarmBroadcaster.init(sub.nh, "mission-kill")
    yield ab.raise_alarm()
    fprint("SQUARE MISSION COMPLETE", msg_color="green")







@txros.util.cancellableInlineCallbacks
def _check_for_run(sub, nh, alarm):
    ''' Waits for the network loss alarm to trigger before '''
    if (yield nh.has_param("autonomous")) and (yield nh.get_param("autonomous")):
        fprint("Preparing to go...")
        yield nh.sleep(5)
        yield do_mission(sub)
    else:
        fprint("Network loss deteceted but NOT starting mission.", msg_color='red')


@txros.util.cancellableInlineCallbacks
def _auto_param_watchdog(nh):
    ''' Watch the `autonomous` param and notify the user when events happen  '''
    ready = False
    while True:
        yield nh.sleep(0.1)

        if not (yield nh.has_param("autonomous")):
            if ready:
                ready = False
                fprint("Autonomous mission disarmed.")
            continue

        if (yield nh.get_param("autonomous")) and not ready:
            ready = True
            fprint("Autonomous mission armed. Disconnect now to run.", msg_color="yellow")

        elif not (yield nh.get_param("autonomous")) and ready:
            ready = False
            fprint("Autonomous mission disarmed.")


@txros.util.cancellableInlineCallbacks
def run(sub):
    al = yield TxAlarmListener.init(sub.nh, "network-loss")
    _auto_param_watchdog(sub.nh)

    call_with_sub = lambda *args: _check_for_run(sub, *args)
    al.add_callback(call_with_sub, call_when_cleared=False)

    fprint("Waiting for network-loss...", msg_color="blue")
    yield defer.Deferred()
