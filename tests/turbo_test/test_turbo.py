import asyncio
import base64
import dataclasses
import math
import random
import time

import aiohttp


@dataclasses.dataclass
class ClickData:
    """
        {
        "ok": true,
        "data": [
            {
                "id": 1657956,
                "userId": 1659140,
                "teamId": 4,
                "leagueId": 3,
                "limitCoins": 6000,
                "totalCoins": "357549",
                "balanceCoins": 70249,
                "spentCoins": 2070300,
                "miningPerTime": 4,
                "multipleClicks": 11,
                "autoClicks": 12,
                "withRobot": true,
                "lastMiningAt": "2024-01-08T15:16:23.000Z",
                "lastAvailableCoins": 5281,
                "turboTimes": 0,
                "avatar": "https://cobuild.ams3.cdn.digitaloceanspaces.com/api-clicker/tg/avatars/1659140.jpg",
                "createdAt": "2023-11-07T22:47:49.000Z",
                "hash": [
                    "TWF0aC5wb3coMywgMyk="
                ],
                "availableCoins": 5468
            }
        ]
    }
    """

    id: int
    userId: int
    teamId: int
    leagueId: int
    limitCoins: int
    totalCoins: str
    balanceCoins: int
    spentCoins: int
    miningPerTime: int
    multipleClicks: int
    autoClicks: int
    withRobot: bool
    lastMiningAt: str
    lastAvailableCoins: int
    turboTimes: int
    avatar: str
    createdAt: str
    hash: list[str] | str
    availableCoins: int


@dataclasses.dataclass
class UserData:
    """
    "user": {
        "id": 1659140,
        "telegramId": "366710566",
        "username": "vffuunnyy",
        "firstName": "有毒なたわごと",
        "lastName": null,
        "locale": "ru",
        "friendlyAddress": null,
        "isPremium": true,
        "isBlocked": false,
        "isForceBlocked": false,
        "role": "user",
        "payload": null,
        "lastNotifiedAt": "2024-01-10T12:34:19.000Z",
        "createdAt": "2023-11-07T22:47:37.000Z",
        "touchedAfterNotification": true,
        "deletedAt": "2024-01-09T09:43:13.792Z"
    },
    """

    id: int
    telegramId: str
    username: str
    firstName: str
    lastName: str | None
    locale: str
    friendlyAddress: str | None
    isPremium: bool
    isBlocked: bool
    isForceBlocked: bool
    role: str
    payload: str | None
    lastNotifiedAt: str
    createdAt: str
    touchedAfterNotification: bool
    deletedAt: str


@dataclasses.dataclass
class ProfileData:
    """
    {
        "ok": true,
        "data": [
            {
                "user": {
                    "id": 1659140,
                    "telegramId": "366710566",
                    "username": "vffuunnyy",
                    "firstName": "有毒なたわごと",
                    "lastName": null,
                    "locale": "ru",
                    "friendlyAddress": null,
                    "isPremium": true,
                    "isBlocked": false,
                    "isForceBlocked": false,
                    "role": "user",
                    "payload": null,
                    "lastNotifiedAt": "2024-01-10T12:34:19.000Z",
                    "createdAt": "2023-11-07T22:47:37.000Z",
                    "touchedAfterNotification": true,
                    "deletedAt": "2024-01-09T09:43:13.792Z"
                },
                "id": 1657956,
                "userId": 1659140,
                "teamId": 577708,
                "leagueId": 3,
                "limitCoins": 6000,
                "totalCoins": "1048165",
                "balanceCoins": 760865,
                "spentCoins": 2070300,
                "miningPerTime": 4,
                "multipleClicks": 11,
                "autoClicks": 12,
                "withRobot": true,
                "lastMiningAt": "2024-01-10T12:47:22.000Z",
                "lastAvailableCoins": 12,
                "turboTimes": 0,
                "avatar": "https://cobuild.ams3.cdn.digitaloceanspaces.com/api-clicker/tg/avatars/1659140.jpg",
                "createdAt": "2023-11-07T22:47:49.000Z",
                "clickerBoostXProfile": [
                    {
                        "id": 15956255,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:29.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15956333,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:31.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15956428,
                        "profileId": 1657956,
                        "boostId": 2,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:34.000Z",
                        "clickerBoost": {
                            "id": 2,
                            "name": "Speed Booster +1",
                            "description": "Increases the restoration speed by 1 click per second",
                            "type": "speedPerHour",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 3,
                            "coefficient": 10,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:31:38.000Z"
                        }
                    },
                    {
                        "id": 15956485,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:36.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15956885,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:50.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15956968,
                        "profileId": 1657956,
                        "boostId": 2,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:53.000Z",
                        "clickerBoost": {
                            "id": 2,
                            "name": "Speed Booster +1",
                            "description": "Increases the restoration speed by 1 click per second",
                            "type": "speedPerHour",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 3,
                            "coefficient": 10,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:31:38.000Z"
                        }
                    },
                    {
                        "id": 15957034,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:34:56.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15958269,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:35:35.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15958355,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:35:38.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15958456,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:35:41.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15958533,
                        "profileId": 1657956,
                        "boostId": 2,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:35:43.000Z",
                        "clickerBoost": {
                            "id": 2,
                            "name": "Speed Booster +1",
                            "description": "Increases the restoration speed by 1 click per second",
                            "type": "speedPerHour",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 3,
                            "coefficient": 10,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:31:38.000Z"
                        }
                    },
                    {
                        "id": 15958625,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:35:46.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15959522,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:36:19.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15959628,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:36:22.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15960913,
                        "profileId": 1657956,
                        "boostId": 18,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:37:05.000Z",
                        "clickerBoost": {
                            "id": 18,
                            "name": "Clicker AI",
                            "description": "How much would you like to mine today, sir?",
                            "type": "robot",
                            "image": null,
                            "coins": 1,
                            "price": 10000,
                            "max": 1,
                            "coefficient": 1,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 2,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 15965101,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:39:11.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15971703,
                        "profileId": 1657956,
                        "boostId": 38,
                        "value": 100000,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:42:27.000Z",
                        "clickerBoost": {
                            "id": 38,
                            "name": "Follow Open Builders",
                            "description": null,
                            "type": "challengeCompleted",
                            "image": null,
                            "coins": 100000,
                            "price": 0,
                            "max": 1,
                            "coefficient": 3,
                            "isPartner": true,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 2,
                            "challengeId": 138,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-12-30T11:55:34.000Z"
                        }
                    },
                    {
                        "id": 15972933,
                        "profileId": 1657956,
                        "boostId": 37,
                        "value": 100000,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:43:04.000Z",
                        "clickerBoost": {
                            "id": 37,
                            "name": "Tonstarter Launchpad",
                            "description": null,
                            "type": "challengeCompleted",
                            "image": null,
                            "coins": 100000,
                            "price": 0,
                            "max": 1,
                            "coefficient": 3,
                            "isPartner": true,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 2,
                            "challengeId": 146,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-12-30T11:55:34.000Z"
                        }
                    },
                    {
                        "id": 15973710,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:43:27.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15975165,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:44:09.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15975271,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:44:12.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15975354,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:44:14.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 15975426,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T05:44:16.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 16120128,
                        "profileId": 1657956,
                        "boostId": 3,
                        "value": 1,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-07T06:47:16.000Z",
                        "clickerBoost": {
                            "id": 3,
                            "name": "Click Booster +1",
                            "description": "Increases the click booster",
                            "type": "multipleClicks",
                            "image": null,
                            "coins": 1,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 3,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 21109470,
                        "profileId": 1657956,
                        "boostId": 13,
                        "value": 100000,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-08T07:45:11.000Z",
                        "clickerBoost": {
                            "id": 13,
                            "name": "Telegram Premium",
                            "description": "Subscribe to get more value from Telegram",
                            "type": "challengeCompleted",
                            "image": "https://cdn.joincommunity.xyz/notcoin/tgPrem.jpeg",
                            "coins": 100000,
                            "price": 0,
                            "max": 1,
                            "coefficient": 3,
                            "isPartner": true,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 2,
                            "challengeId": 71,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-18T17:35:24.000Z"
                        }
                    },
                    {
                        "id": 21129568,
                        "profileId": 1657956,
                        "boostId": 34,
                        "value": 100000,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-08T07:50:14.000Z",
                        "clickerBoost": {
                            "id": 34,
                            "name": "GT Protocol Campaign",
                            "description": null,
                            "type": "challengeCompleted",
                            "image": null,
                            "coins": 100000,
                            "price": 0,
                            "max": 1,
                            "coefficient": 3,
                            "isPartner": true,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "inactive",
                            "minLeagueId": 2,
                            "challengeId": 73,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-12-30T11:55:34.000Z"
                        }
                    },
                    {
                        "id": 21132223,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-08T07:50:56.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    },
                    {
                        "id": 23006221,
                        "profileId": 1657956,
                        "boostId": 1,
                        "value": 500,
                        "status": "active",
                        "expiresAt": null,
                        "isApplied": true,
                        "isExpired": false,
                        "createdAt": "2024-01-08T15:01:42.000Z",
                        "clickerBoost": {
                            "id": 1,
                            "name": "Energy Limit +500",
                            "description": "Increases the click limit by 50 ",
                            "type": "increaseLimit",
                            "image": null,
                            "coins": 500,
                            "price": 1000,
                            "max": 10000,
                            "coefficient": 7,
                            "isPartner": false,
                            "isTask": false,
                            "isFeatured": false,
                            "status": "active",
                            "minLeagueId": 1,
                            "challengeId": null,
                            "liveTimeInSeconds": null,
                            "createdAt": "2023-08-17T21:09:49.000Z"
                        }
                    }
                ],
                "clickerTeam": {
                    "id": 577708,
                    "name": "WebM⚡️2.0",
                    "slug": "@webmland",
                    "chatId": 580682,
                    "leagueId": 3,
                    "logo": "https://cdn.joincommunity.xyz/api-clicker/tg/team-avatars/580682.jpg",
                    "coins": "110532891",
                    "createdAt": "2024-01-07T18:38:07.000Z"
                },
                "availableCoins": 6000
            }
        ]
    }
    """

    user: UserData | dict
    id: int
    userId: int
    teamId: int
    leagueId: int
    limitCoins: int
    totalCoins: int
    balanceCoins: int
    spentCoins: int
    miningPerTime: int
    multipleClicks: int
    autoClicks: int
    withRobot: bool
    lastMiningAt: str
    lastAvailableCoins: int
    turboTimes: int
    avatar: str
    createdAt: str
    availableCoins: int


headers = {
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Android WebView";v="120"',
    "DNT": "1",
    "Sec-Ch-Ua-Mobile": "?1",
    "X-Requested-With": "org.telegram.messenger.web",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SY Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Auth": "1",
    "Accept": "application/json",
    "Referer": "https://clicker.joincommunity.xyz/",
    "Sec-Ch-Ua-Platform": '"Android"',
}


async def send_request(
    url: str, data: dict | None = None, method: str = "post"
) -> dict | list | int | None:
    async with aiohttp.ClientSession() as session:
        with open("access_token.txt", encoding="utf-8") as f:
            access_token = f.read()
            headers["Authorization"] = f"Bearer {access_token}"

        if data:
            headers["Content-Type"] = "application/json"
        else:
            headers.pop("Content-Type", None)

        async with session.request(
            method,
            url,
            headers=headers,
            json=data if data else None,
            skip_auto_headers=["Content-Type"],
        ) as response:
            if 200 <= response.status < 300:
                result = await response.json()

                if result.get("ok") and result.get("data") is not None:
                    return result.get("data")
                else:
                    print(result)
                    return result.get("data", result)
            else:
                print("Error:", response.status)
                print(await response.text())
                return None


async def get_profile():
    result = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/profile", method="get"
    )

    if result:
        profile = ProfileData(
            **{k: v for k, v in result[0].items() if k in ProfileData.__annotations__}
        )
        profile.user = UserData(
            **{k: v for k, v in profile.user.items() if k in UserData.__annotations__}
        )

        print(
            "User:",
            profile.user.username,
            profile.user.id,
            profile.user.firstName,
            profile.user.lastName,
        )
        print("Mining per click:", profile.multipleClicks)
        print("Mining per sec:", profile.miningPerTime)
        print("Available coins:", profile.availableCoins)
        print("Balance coins:", profile.balanceCoins)
        print("Total coins:", profile.totalCoins)

        profile.totalCoins = int(profile.totalCoins)

        return profile
    return None


async def get_store() -> dict:
    store = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/store/merged", method="get"
    )

    multiple_clicks: dict = {}
    speed_per_hour_booster: dict = {}
    increase_limit_booster: dict = {}

    for booster in store:
        match booster.get("id"):
            case 1:
                increase_limit_booster = booster
                print("Increase limit booster price:", booster.get("price"))
            case 2:
                speed_per_hour_booster = booster
                print("Speed per hour booster price:", booster.get("price"))
            case 3:
                multiple_clicks = booster
                print("Multiple clicks booster price:", booster.get("price"))
            # case 18:
            #     print("Clicker AI booster price:", booster.get("price"))

    return {
        "increase_limit_booster": increase_limit_booster,
        "speed_per_hour_booster": speed_per_hour_booster,
        "multiple_clicks": multiple_clicks,
    }


async def check_robot() -> int:
    robot_count = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/core/robot", method="get"
    )

    print("Robot count:", robot_count)
    return robot_count


async def claim_robot() -> dict:
    result = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/core/robot", method="post"
    )

    print("Robot claimed")
    return result


async def check_tasks() -> list:
    result = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/task/combine-completed", method="get"
    )
    completed_tasks = []

    for task in result:
        if task.get("taskId") in {
            2,  # Recover full energy
            3,  # Claim free turbo
            # 4,  # Get bonus for first 1000 clicks
            # 5,  # Get bonus for 10 referrals,
            6,  # Get bonus for joinsquad
            7,  # Get bonus for Silver league
            8,  # Get bonus for Gold league
        }:
            completed_tasks.append(task)

    return completed_tasks


async def complete_task(task_id: int) -> dict:
    result = await send_request(
        f"https://clicker-api.joincommunity.xyz/clicker/task/{task_id}", method="post"
    )

    print("Task completed")
    return result


async def activate_turbo() -> dict:
    result = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/core/active-turbo", method="post"
    )

    if result:
        print("Turbo activated")
    return result


def can_buy_booster(booster: dict, coins_balance: int) -> bool:
    return booster.get("price") <= coins_balance and booster.get("max") > booster.get("count")


def calc_hash(hash_expression):
    hash_expression = hash_expression.strip()

    if "Math" in hash_expression:
        try:
            hash_expression = (
                hash_expression.replace("Math", "math")
                .replace("math.abs", "abs")
                .replace("math.PI", "math.pi")
                .replace("math.max", "max")
                .replace("math.min", "min")
            )

            return int(eval(hash_expression, {"math": __import__("math")}))
        except:
            return 0
    elif "?" in hash_expression and ":" in hash_expression:
        return int(hash_expression.split("?")[1].split(":")[0].strip())
    elif hash_expression.isdigit():
        return int(hash_expression)
    elif hash_expression == "document.querySelectorAll('body').length":
        return 1
    else:
        return random.randint(0, 10000)


def clicks_per_request(available_coins: int, mining_per_click: int) -> int:
    return min(math.floor(available_coins / mining_per_click), 159)


async def turbo_loop(profile: ProfileData, evaluated_hash: int | None = None) -> tuple:
    if profile.turboTimes > 1:
        activate_turbo_result = await activate_turbo()
        multiple = activate_turbo_result[0].get("multiple")
        clicks_count = random.randint(20, 24)

        for i in range(5):
            await asyncio.sleep(1.75)

            with open("webapp_data.txt", encoding="utf-8") as f:
                data = {
                    "count": clicks_count * profile.multipleClicks * multiple,
                    "turbo": True,
                    "webAppData": f.read(),
                }

            print("Request:", i + 1)
            print(
                "Clicks count:",
                clicks_count,
                "(",
                clicks_count * profile.multipleClicks * multiple,
                ")",
            )

            if evaluated_hash:
                data["hash"] = evaluated_hash

            result = await send_request(
                "https://clicker-api.joincommunity.xyz/clicker/core/click", data
            )

            if not result:
                break

            if isinstance(result, dict) and result.get("statusCode") == 400:
                profile.turboTimes -= 1
                print(result.get("message"))
                break

            result = ClickData(
                **{k: v for k, v in result[0].items() if k in ClickData.__annotations__}
            )
            result.hash = [base64.b64decode(h).decode("utf-8") for h in result.hash]

            evaluated_hash = sum(map(calc_hash, result.hash))

            if not evaluated_hash:
                evaluated_hash = None

            print("Evaluated hash:", evaluated_hash)
            print("Balance coins:", result.balanceCoins)

            profile.turboTimes = result.turboTimes

    return profile, evaluated_hash


async def check_turbo() -> int:
    result = await send_request(
        "https://clicker-api.joincommunity.xyz/clicker/core/check-turbo", method="post"
    )

    if not result:
        return -1

    if result.get("turbo"):
        print("Turbo is active")
        return 1

    if result.get("message") == "Try later":
        print("Turbo > Try later")
        return -1

    print("No turbo yet")
    return 0


async def click(
    count: int, webapp_data: str, evaluated_hash: int | None, multiply: int = 1
) -> tuple[int | None, int | None, str | None]:
    data = {
        "count": count * multiply,
        "webAppData": webapp_data,
    }

    if multiply > 1:
        data["turbo"] = True

    if evaluated_hash:
        data["hash"] = evaluated_hash

    result = await send_request("https://clicker-api.joincommunity.xyz/clicker/core/click", data)

    if not result:
        print("Bad Click")
        return None, None, None

    result = ClickData(**{k: v for k, v in result[0].items() if k in ClickData.__annotations__})
    result.hash = [base64.b64decode(h).decode("utf-8") for h in result.hash]

    evaluated_hash = sum(map(calc_hash, result.hash))

    if not evaluated_hash:
        evaluated_hash = None

    print("Nice click awesome balls")
    return result.availableCoins, result.balanceCoins, evaluated_hash


async def main() -> None:
    evaluated_hash = None
    profile = await get_profile()
    next_turbo_check = time.time()

    while True:
        multiple = 1
        clicks_count = math.ceil(profile.multipleClicks / profile.miningPerTime)

        with open("webapp_data.txt", encoding="utf-8") as f:
            webapp_data = f.read()

        if next_turbo_check < time.time():
            turbo_result = await check_turbo()

            if turbo_result == 1:
                activation_result = await activate_turbo()

                if isinstance(activation_result, list):
                    multiple = activation_result[0].get("multiple")
                    expire = activation_result[0].get("expire")

                    clicks_count = random.randint(150, 159)  # noqa: S311

                    print("Multiple:", multiple, "| Score:", clicks_count * multiple * profile.multipleClicks)
                    print("Waiting:", sleep_time := (expire / 1000 - time.time() - 2))
                    await asyncio.sleep(sleep_time)

                    next_turbo_check = time.time() + 10
            elif turbo_result == -1:
                next_turbo_check = time.time() + 30
            else:
                next_turbo_check = time.time() + 10

        print("Clicks count:", clicks_count, "(", clicks_count * profile.multipleClicks, ")")

        available_coins, balance_coins, evaluated_hash = await click(
            clicks_count * profile.multipleClicks, webapp_data, evaluated_hash, multiple
        )

        print("Evaluated hash:", evaluated_hash)
        print("Available coins:", available_coins)
        print("Balance coins:", balance_coins)

        profile.availableCoins = available_coins
        profile.balanceCoins = balance_coins

        await asyncio.sleep(profile.miningPerTime)

        print()


asyncio.run(main())
