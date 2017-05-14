'use strict';
const moment = require('moment');
const fs = require('fs');

const posts = [
    {
        name: 'Transfigure',
        url: 'http://transfigure.bbcdigitalguerrillas.co.uk/',
        date: moment('2015-09-01')
    },
    {
        name: 'Thirteen: Find the Girl',
        url: 'http://blog.findthegirl.co.uk/',
        date: moment('2016-02-28')
    },
    {
        name: 'Mates vs Monsters',
        url: 'http://matesvsmonsters.bbcdigitalguerrillas.co.uk/',
        date: moment('2016-10-01')
    },
    {
        name: 'SofaSync',
        date: moment('2016-11-01')
    },
    {
        name: 'YouTube Dubber',
        url: 'http://youtubedubber.bbcdigitalguerrillas.co.uk/',
        date: moment('2016-12-01')
    },
    {
        name: 'NewsRush',
        url: 'newsrush.bbcdigitalguerrillas.co.uk',
        date: moment('2015-08-01')
    },
    {
        name: 'Rhubarb Crumble',
        url: 'https://github.com/mattandrews/rhubarb-crumble',
        date: moment('2017-02-01')
    },
    {
        name: 'What is That?',
        url: 'http://whatisthat.bbcdigitalguerrillas.co.uk/?preview',
        date: moment('2016-04-01')
    },
    {
        name: 'I\'m a Pretender',
        url: 'http://threechords.org/pretender/',
        date: moment('2012-03-01')
    },
    {
        name: 'Gygax',
        url: 'https://github.com/mattandrews/gygax',
        date: moment('2016-11-01')
    },
    {
        name: 'Off The Record',
        url: 'http://offtherecord.club',
        date: moment('2015-02-01')
    },
    {
        name: 'Scene Point Blank',
        url: 'https://www.scenepointblank.com',
        date: moment('2003-03-01')
    },
    {
        name: 'Snow Messages',
        url: 'http://mattandrews.info:8000/',
        date: moment('2016-12-01')
    },
    {
        name: 'Who Voted What',
        url: 'http://whovotedwhat.co.uk/',
        date: moment('2012-04-01')
    }
];

const slugify = function (text) {
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
};

const writeFile = function (path, contents) {
    fs.writeFile(path, contents, function(err) {
        if(err) {
            return console.log(err);
        }
        console.log("The file was saved! " + path);
    });
};

const makeDate = function (date) {
    return {
        filename: moment(date).format('YYYY-MM-DD'),
        str: moment(date).format('YYYY-MM-DD 00:00:00')
    }
};

const makePost = function (p) {
    let str = `---
layout: post
categories: portfolio
title: ${p.name}
date: ${p.date.str}`;
    if (p.url) {
        str += `
link: ${p.url}
`;
    }
str += `---`;
    return str;
};

posts.forEach(p => {
    p.date = makeDate(p.date);
    let content = makePost(p);
    let filename = p.date.filename + '-' + slugify(p.name) + '.html';
    let dir = './_posts/portfolio/';
    writeFile(dir + filename, content);
});