// KNOWN ISSUE: The flashing green for accepting an offer doesn't always line up on the offer you accepted,
// so for the time being I have simply disabled it

// KNOWN ISSUE: If you accept an offer that is not the most current offer, it will be re-submitted
// and the other player will have the option not to take it.

//This is a JavaScript script for handling the countdown;
//is there a reason we couldn't just use oTree's built-in countdown?
$(function() {
    if (seconds_to_start > 0) {
	$('.otree-timer').css({"display": "none"})
    }
    var display = document.getElementById("display");
//    display.innerHTML = "It's not yet time to start.";
    console.log("This should run at the start.");
    var currentDate = new Date();
    var milliseconds = Math.floor(seconds_to_start * 1000);
    $('#start-delay-timer').countdown(currentDate.valueOf() + milliseconds)
	.on('update.countdown', function (event) {
	    // %-N is "Total count of minutes till the end, non-padded"
	    // %S is seconds left
	    var display = document.getElementById("display");
	    display.innerHTML = "";
	    var format = '%-S';
	    $(this).html(event.strftime(format));
	})
	.on('finish.countdown', function (event) {
	    if (daForm) {
		daForm.started = true
	    }
	    $('.otree-timer').css({"display": "block"})
	});
});

//I think this function submits the form and finishes the page
var submitForm = function(event, role, cm, cx, vm, vx, group) {
    var display = document.getElementById("display");
    console.log("This should run when the form is submitted.");
    console.log(event)
    var el = document.getElementById("form");
    if (el.checkValidity()) {
        var formValue = parseFloat(document.querySelector('[name=offer]').value);
        var formQuantity = parseFloat(document.querySelector('[name=quantity]').value);
        var buyerPayoff =  vm * formQuantity ** vx - formValue;
        var sellerPayoff = formValue - cm * formQuantity ** cx;
        var formGroup = group;
//        debugger;
//        Clear values you so can't just spam the same offer; not sure if I really want this
//        document.getElementById('offer').value = 0;
//        document.getElementById('quantity').value = 0;
//        document.getElementById('id_proposed_quantity').innerHTML = "";
//        document.getElementById('id_proposed_price').innerHTML = "";
//        if (player.role==="seller") {
//            var betterBids = data.bids.filter( function(bid) { return bid.value > formValue; });
//        } else {
//            var betterBids = data.asks.filter( function(ask) { return ask.value < formValue; });
//        }
//        if (betterBids.length) {
//            modal.type = "bid";
//            modal.strings = getStringsFor(player.role)
//            modal.value = formValue;
//            modal.quantity = formQuantity;
//            modal.otherValue = betterBids[0].value;
//            modal.result = modal.otherValue;
//            openModal()
//        }
        var bid = {
            value: formValue,
            quantity: formQuantity,
            group: formGroup,
            buyer_payoff: buyerPayoff,
            seller_payoff: sellerPayoff,
        };
//        debugger;
        console.log("This should check if the offer is a valid one to submit.");
        if (!isProfitable(formValue, formQuantity, "buyer", cm, cx, vm, vx))
        {
            if (role == "buyer") {
                var string = "you"
            } else {
                var string = "the buyer"
            }
            display.innerHTML = "You can't make that proposal; it would result in a loss for " + string + ".";
        }
        else if (!isProfitable(formValue, formQuantity, "seller", cm, cx, vm, vx))
        {
            if (role == "seller") {
                var string = "you"
            } else {
                var string = "the seller"
            }
            display.innerHTML = "You can't make that proposal; it would result in a loss for " + string + ".";
        }
        else
        {
            display.innerHTML = "Proposal submitted!";
//        It calls sendmessage to send a message to the socket layer
//        The sender's identity and role is received from the Django template Game.html in the coding of the sendmessage function
            sendmessage(formValue, formQuantity, formGroup, buyerPayoff, sellerPayoff);
        }
    }
    else {
        el.reportValidity()
    }
}

//This function is specific for getting the bids; it is called below
//All it seems to do is generate a dict of three bid-relevant strings
function getStringsFor( type ) {
    return {
        seller: {
            valueType: "ask",
            otherType: "bid",
            comparison: "higher",
        },
        buyer: {
            valueType: "bid",
            otherType: "ask",
            comparison: "lower",
        }
    }[type];
}

//Vue is a user interface class, which apparently is what all these 'modal' objects are
var modal = new Vue({
    el: '#confirmModal',
    data: {
        type: 'accept',
        confirm: false,
        strings: getStringsFor("seller"),
        value: 0,
        quantity: 0,
        group: 0,
        buyer_payoff: 0,
        seller_payoff: 0,
        playerId: null,
        playerIdInGroup: null,
        result: 0,
        otherValue: 0,
    },
    methods: {
        sendIt: function(event) {
            if ( data.bids.filter(bid => bid.id === this.playerId).length || data.asks.filter(ask => ask.id === this.playerId).length )
                sendmessage(this.value, this.quantity, this.group, this.buyer_payoff, this.seller_payoff, this.playerId)
            else {
//            Toastr just sends text notifications to the players
//                toastr.error("Sorry, the offer is not available anymore.")
                closeModal()
            }
        }
    }
})

//This initializes the data on bids; but how are new bids added to the list?
var data = {
    bids: [],
    asks: [],
};

//I guess this tracks player IDs?
var info = new Vue({
    el: '#info',
    data: {
        playerId: player.id
    }
});

//I think var app is like int main() in C++, the main function that gets called
var app = new Vue({
    el: '#app',
    data: {
        table: {
            rows: []
        },
        playerId: player.id,
        playerRole: player.role,
        maxValue: player.maxValue,
        minValue: player.minValue,
        bestBids: {
            seller: 0,
            buyer: 0
        },
        lock: null,
        match: player.match
    },
    methods: {
//    This method accepts a bid and sends a message accordingly
        accept: function(bid) {
            modal.type = "accept";
            modal.playerId = bid.id;
            modal.playerIdInGroup = bid.id_in_group;
            modal.value = bid.value;
            modal.quantity = bid.quantity;
            modal.result = bid.value;
            modal.group = bid.group;
            modal.buyer_payoff = bid.buyer_payoff;
            modal.seller_payoff = bid.seller_payoff;
            // openModal()
            sendmessage(bid.value, bid.quantity, bid.group, bid.buyer_payoff, bid.seller_payoff, bid.id)
        },
//        This method checks whether a bid is valid or not
        isAcceptable: function(entry, entryRole, cm, cx, vm, vx) {
            var otherRole = entryRole === "buyer" ? "seller" : "buyer";
//            var playerHasEnoughValuation = this.playerRole === "buyer" ? entry.value <= this.maxValue : entry.value >= this.minValue;
//            var isBestBid = entry.value === this.bestBids[entryRole];
            var isRoleCorrect = this.playerRole === otherRole;
            var hasNoMatch = !this.match;
            var fairForBuyer = isProfitable(entry.value, entry.quantity, "buyer", cm, cx, vm, vx);
            var fairForSeller = isProfitable(entry.value, entry.quantity, "seller", cm, cx, vm, vx);
            var fairDeal = fairForBuyer && fairForSeller
//            document.getElementById("display").innerHTML = entryRole.concat(",", entry.value, ",", entry.quantity + "," + cl + "," + cq + "," + seller_comparison + "," + vl + "," + vq + "," + buyer_comparison + "," + fairDeal)

        return isRoleCorrect && hasNoMatch && fairDeal;
//            return isRoleCorrect && hasNoMatch;
//            return isRoleCorrect && isBestBid && playerHasEnoughValuation && hasNoMatch;
        },
//          This method checks whether the offer is from within your group
        isSameGroup(entry, group) {
            console.log("isSameGroup: Checking if offer is from within my group.")
            var rightGroup = entry.group == group;
            console.log(entry.group)
            console.log(group)
            console.log(rightGroup)
        return rightGroup;
        }
    },
})
//I think this just stores a table of participants; why do we need it?
//var participantTable = new Vue({
//    el: '#participant_table',
//    data: {
//        participants: player.participants,
//        playerId: player.id
//    }
//})

// My new generalized function for checking if a bid is valid
function isProfitable(value, quantity, role, cm, cx, vm, vx) {
    console.log("isProfitable: Checking if proposal is valid.");
    var buyer_comparison = vm * quantity ** vx;
    var seller_comparison = cm * quantity ** cx;
        if (role == "buyer") {
            return buyer_comparison >= value
        } else {
            return seller_comparison <= value
        }
    }

//Not entirely clear on what this object is doing.
var daForm = new Vue({
    el: '#da_form',
    data: {
        value: player.value,
        quantity: player.quantity,
        group: player.group,
        lock: null,
        started: seconds_to_start > 0 ? false : true,
        match: player.match
    },
    methods: {
//    Submits the form, does not finish the page
        submitForm: submitForm
    }
})

//var nextButton = new Vue({
//    el: '#next_button',
//    data: {
//        done: player.match,
//    },
//})

//A lot of this seems to be matching logic for the bids and asks
function updateDomFromWsObj(obj) {
    console.log("updateDomFromWsObj(obj)")
    console.log(obj)
    switch (obj.type) {
        case "go":
            document.getElementById("form").submit()
            break;

        case "match":

            if (obj.buyer === player.id || obj.seller === player.id) {
                daForm.match = true;
                app.match = true;
//                toastr.success("You are trading!")
            }

            // set match flag on bid and ask
            data.bids.filter( bid => bid.id === obj.buyer)[0].match = true;
            data.asks.filter( ask => ask.id === obj.seller)[0].match = true;

            transformToTable(app.table, data.asks, data.bids)

            // remove ask and bid after 3 sec
            setTimeout( () => {
                data.bids = data.bids.filter( bid => bid.id !== obj.buyer)
                data.asks = data.asks.filter( ask => ask.id !== obj.seller)
                prepareDataForTable(data)
                transformToTable(app.table, data.asks, data.bids)
            }, 3000)

            break;

//'clearing' a bid means making the transaction happen? Or removing it?
        case "clear":
            if (obj.player_id === player.id) {
                daForm.value = null;
                daForm.lock = null;
                app.lock = null;
//                toastr.success("Bid cleared")
            }
            data.bids = data.bids.filter( elem => {
                return elem.id !== obj.player_id;
            })
            data.asks = data.asks.filter( elem => {
                return elem.id !== obj.player_id;
            })
            break;

        case "error":
            if (player.role==="buyer") {
//                toastr.error("There is a better bid than yours")
            } else {
//                toastr.error("There is a lower offer")
            }
            break;

        case "status":
            participantTable.participants.forEach( function(p) {
                if (p[0].id === obj.player_id) {
                    p[0].status = obj.status;
                } else if (p[1].id === obj.player_id) {
                    p[1].status = obj.status;
                }
            })
            break;

        default:

            updateOrCreate(data, obj)
            if (obj.player_id === player.id) {
                daForm.lock = true;
                app.lock = true;
                daForm.value = obj.value;
                daForm.quantity = obj.quantity;
                daForm.group = obj.group;
                daForm.buyer_payoff = obj.buyer_payoff;
                daForm.seller_payoff = obj.seller_payoff;
            }
    }

    prepareDataForTable(data)
    transformToTable(app.table, data.asks, data.bids)


    // console.log(app)
    console.log(data)
    // #console.log("player ", player);
}

//This is to convert the bid-ask data into a table
function transformToTable(table, row1, row2) {
    table.rows = [];
    for (var i=0; i<Math.max(row1.length, row2.length); i++) {


        var r1 = row1[i] ? row1[i] : null;
        var r2 = row2[i] ? row2[i] : null;

        table.rows.push({
            r1: r1,
            r2: r2
        })

    }
}

//This is to make or update the list of bids
//I may need to change this to handle multiple offers
function updateOrCreate(list, obj) {
//    console.log("Update or create list for table")
//    console.log(list)
//    console.log(obj)
    key = obj.type === "seller" ? "asks" : "bids";
//    var existingElement = list[key].filter(el => el.id === obj.player_id)[0] || null;
//
//    if (existingElement) {
//        existingElement.value = obj.value;
//        existingElement.quantity = obj.quantity;
//    }
//    else {
        list[key].push({
            id: obj.player_id,
            id_in_group: obj.player_id_in_group,
            value: obj.value,
            quantity: obj.quantity,
            group: obj.group,
            buyer_payoff: obj.buyer_payoff,
            seller_payoff: obj.seller_payoff,
        })
//    }

}

//This prepares the bid-ask data to be put into a table
function prepareDataForTable(data) {
//    calculateBestBids(data, "seller")
//    calculateBestBids(data, "buyer")

//    This doesn't seem to work
//    data.bids = removeDuplicates(data.bids)
//    data.asks = removeDuplicates(data.asks)

//    data.bids.sort( function(a, b) {
//        return a.value-b.value
//    })
//    data.asks.sort( function(a, b) {
//        return b.value-a.value
//    })
}

//This determines which bids are highest and lowest
function calculateBestBids(data, type) {
    key = type === "seller" ? "asks" : "bids";
    minOrMax = type === "seller" ? "min" : "max";
    app.bestBids[type] = Math[minOrMax].apply(
        null,
        data[key]
            .filter( function (dataElement) { return !dataElement.match })
            .map( function (dataElement) { return dataElement.value; } ));
}

//function removeDuplicates(items) {
//  let unique = {};
//  let result = {};
//  items.forEach(function(i) {
//    if(!unique.includes([i.value, i.quantity])) {
//      unique.concat([[i.value, i.quantity]])
//      result.concat([i])
//    }
//  });
//  return result;
//}

//I have no idea what 'modals' are or what they are being used for
function openModal() {
    $('#confirmModal').modal();
}
function closeModal() {
    $('#confirmModal').modal('hide');
}

