const s_tag = '<script>', e_tag = '</script>';

const get_generator = page =>  {
    const s_ind = page.indexOf(s_tag);
    const e_ind = page.indexOf(e_tag);

    let code = page.substring(s_ind + s_tag.length, e_ind);
    const e_brack = code.lastIndexOf('}');

    code = code.substring(0, e_brack);
    code += '"r";';

    console.log('Primary\n', code);

    let secondary = eval(code);
    // console.log(secondary);
}

module.exports = {
    get_generator
};
