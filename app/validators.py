from app import app, db
from app.models import User, Reservation, Classroom
from datetime import datetime

def validateTime(fro, to, startdate, enddate, classroom):
    roomReservations = Classroom.query.filter_by(id=classroom).first().reservations.order_by(Reservation.fromTime).all()
    for i in range(len(roomReservations)):
        reserv = roomReservations[i]
        if startdate > reserv.toTime.date() or enddate < reserv.fromTime.date():
            pass
        elif (startdate == reserv.toTime.date() and enddate == reserv.toTime.date()) or startdate == reserv.toTime.date():
            if fro.hour > reserv.toTime.time().hour or to.hour < reserv.fromTime.time().hour:
                pass
            elif fro.hour == reserv.toTime.time().hour:
                if fro.minute > reserv.toTime.time().minute:
                    pass
                else:

                    return 'This time is already reserved, reservation is from: '+str(reserv.fromTime)+" to: "+str(roomReservations[i].toTime)
            else:
                return 'This time is already reserved, reservation is from: '+str(reserv.fromTime)+" to: "+str(roomReservations[i].toTime)
        else:
            return 'This time is already reserved, reservation is from: '+str(reserv.fromTime)+" to: "+str(roomReservations[i].toTime)
    return True

def validateLength(fro, to, startdate, enddate):
    if enddate.day-startdate.day> 5 or enddate.month != startdate.month or enddate.year != startdate.year:
        return 'Reservations are only available for a period of 1 hour to 5 days'
    if startdate==enddate and to.hour-fro.hour < 1 :
        return 'Reservations are only available for a period of 1 hour to 5 days'
    elif to.hour - fro.hour == 1:
        if(to.minute>=fro.minute):
            return True
        else:
            return 'Reservations are only available for a period of 1 hour to 5 days'
    return True


def validate_Date(fro, to, startdate, enddate):
    now = datetime.now()
    if startdate < enddate:
        print("Error in choosing date")
    elif startdate == enddate:
        if fro.hour < to.hour:
            print("Error in choosing hours")
        elif fro.hour == to.hour:
            if fro.minute <= to.minute:
                print("Error in choosing minutes")

    if startdate < now.date() :
        return "You can't reserve for past time"
    elif startdate == now.date():
        if fro.hour < now.time().hour:
            return "You can't reserve for past time"
        elif fro.hour == now.time().hour:
            if fro.minute < now.time().minute:
                return "You can't reserve for past time"
    return True



def validate_delay(current_user):
    now = datetime.now()
    reservs = current_user.reservations.all()
    for res in reservs:
        if res.toTime.date() < now.date():
            reservs.remove(res)
        elif res.toTime.date() == now.date():
            if res.toTime.time() < now.time():
                reservs.remove(res)
    return reservs


